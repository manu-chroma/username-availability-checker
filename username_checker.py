import re
import logging
import os
import uuid
import sys
import json

import requests as r
import yaml
from requests_toolbelt.utils import dump
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template
from flask.ext.cors import CORS, cross_origin
from werkzeug.contrib.cache import SimpleCache
from dotenv import load_dotenv

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv('.env')
HOST_BACKEND = os.environ.get('HOST_BACKEND')
PORT_BACKEND = os.environ.get('PORT_BACKEND')
PORT_FRONTEND = os.environ.get('PORT_FRONTEND')
PROTOCOL_BACKEND = os.environ.get('PROTOCOL_BACKEND')

patterns = yaml.load(open('websites.yml'))

sites = ' '.join(list(patterns['username_patterns'].keys()))
logos = json.dumps(patterns['logos'])

cache = SimpleCache()

# This session is for injecting cookies into requests
# Discussion: github.com/manu-chroma/username-availability-checker/issues/79
session = r.Session()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] '
                              '%(asctime)s %(message)s')
handler.setLevel(logging.WARNING)
handler.setFormatter(formatter)
logger.addHandler(handler)


class DebugFilter(logging.Filter):
    """
    DebugFilter only logs if class variable DEBUG is True.
    """

    DEBUG = False

    def filter(self, record):
        return DebugFilter.DEBUG  # assumes that DEBUG is always boolean


logger.addFilter(DebugFilter())


def log_response(msg, response, website, username):
    """
    Dump response and log message with warning level.

    requests_toolbet.utils.dump.dump_all is used for dumping response.
    The dump file will be located under statics/errors.
    Also, the file name will be {website}_{username}_{id}.dump.
    Generate directory if it doesn't exist.
    """
    # Generates unique id for this response.
    id = uuid.uuid4().hex

    filename = 'static/errors/{}_{}_{}.dump'.format(website, username, id)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        # Note: https://toolbelt.readthedocs.io/en/latest/dumputils.html
        f.write(dump.dump_all(response).decode('utf-8'))

    logger.warning('%s\nid: %s', msg, id)


def get_profile_url(website, username):
    return patterns['urls'].get(website, 'https://{w}.com/{u}').format(
        w=website,
        u=username
    )


def get_avatar(website, username):
    data = patterns['avatar'][website]

    if not data:
        logger.warning('There is no avatar data for {}'.format(website))
        return None

    url = get_profile_url(website, username)
    if 'url' in data:
        url = data['url'].format(u=username)

    response = session.get(url)
    if response.status_code == 404:
        log_response(
            'Status code of response for {}/{} is 404'.format(website, username),
            response,
            website,
            username)
        return None

    if data == 'opengraph':
        # Look in metadata for image.
        soup = BeautifulSoup(response.text, 'html.parser')
        result = [item.attrs['content'] for item in soup('meta')
                  if item.has_attr('property') and
                  item.attrs['property'].lower() == 'og:image']
        if not result or not result[0]:
            log_response(
                'There is no opengraph image found for {}/{}'.format(
                    website, username),
                response,
                website,
                username)
            return None
        result = result[0]
    elif 'html_selector' in data:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.select(data['html_selector'])
        if website == 'gravatar':
            src = images[0]['href']
        else:
            src = images[0]['src']
        return src
    elif 'key' in data:
        # Searches for "`key`": "`link`"
        regex = re.compile('[\'\"]' + re.escape(data['key']) +
                           r'[\'\"]:(\s)?[\'\"](?P<link>[^\s]+)[\'\"]')
        result = re.search(regex, response.text)
        if not result:
            log_response(
                'There is no match found for {}/{}'.format(website, username),
                response,
                website,
                username)
            return None
        result = result.group('link')
    elif response.headers.get('content-type', '').startswith('image/'):
        return url
    else:
        log_response(
            'Unexpected result: {}/{}'.format(website, username),
            response,
            website,
            username)
        return None

    # Fix relative links
    if result[0] == '/':
        base_url = get_profile_url(website, '')
        result = base_url + result
    return result


def get_status_code(website, username):
    url = get_profile_url(website, username)

    if website in patterns['content_verification']:
        res = session.get(url)
        phrase = patterns['content_verification'][website].format(u=username)
        if bytes(phrase, encoding='utf-8') in res.content:
            return 200
        else:
            return 404

    else:
        return session.get(url).status_code


def check_username(website, username):
    url = get_profile_url(website, username)

    usable = check_usable(website)

    possible = check_format(website, username)

    if not usable:
        return {
            'url': url,
            'possible': possible,
            'usable': usable,
        }

    if not possible:
        return {
            'url': url,
            'possible': possible,
            'usable': usable,
        }

    code = get_status_code(website, username)

    if website in patterns['content_verification']:

        return {
            'status': code,
            'url': url,
            'avatar': get_avatar(website, username) if code == 200
            else None,
            'possible': possible,
            'usable': usable,
        }

    elif website == 'facebook':
        res = session.get(url)

        # Using mfacebook for checking username,
        # when a username exists but hidden from
        # search engines, it gives a login redirect
        # and 200 code but in case of no profile
        # available, gives a 404 error.

        if len(res.history) > 0 and code == 200:
            profile = 'hidden'
        else:
            profile = 'visible'

        return {
            'status': code,
            'url': url,
            'avatar': get_avatar(website, username),
            'possible': possible,
            'profile': profile,
            'usable': usable,
        }

    else:
        return {
            'status': session.get(url).status_code,
            'url': url,
            'avatar': get_avatar(website, username),
            'possible': possible,
            'usable': usable,
        }


def check_usable(website):
    """
    Check if the website is usable.

    It works by checking if known taken username is shown as available.
    The checking will be cached in memory for 10 minutes.
    """
    identifier = 'usable_{}'.format(website)

    usable = cache.get(identifier)
    if usable is not None:
        return usable

    constant_username = patterns['constant_usernames'][website]

    code = get_status_code(website, constant_username)

    if code == 404 or code == 301:
        usable = False
    else:
        usable = True
    cache.set(identifier, usable, timeout=60*10)

    return usable


def check_format(website, username):
    """
    Check the format of a username depending on the website.
    """
    website_parts = patterns['username_patterns'][website]

    if 'invalid_patterns' in website_parts:
        for invalid_pattern in website_parts['invalid_patterns']:
            invalid_matches = re.search(invalid_pattern, username)

            if invalid_matches is not None:
                return False

    pattern = r'^[{chars}]{{{min},{max}}}$'.format(
        chars=website_parts['characters'],
        min=website_parts['min_length'],
        max=website_parts['max_length']
    )

    matches = re.match(pattern, username)

    if website == 'facebook':
        # enforce 5 char limit excluding '.'
        # for facebook
        username = username.replace('.', '')

        if len(username) <= 5:
            return False

    if matches is not None:
        return True
    else:
        return False

# API endpoints


@app.route('/api/')
@cross_origin(origin='*')
def hello():
    return 'Hello world! The app seems to be working!'


@app.route('/api/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check(website, username):
    return jsonify(check_username(website, username))
    
# frontend
@app.route('/', methods=['GET'])
@cross_origin()
def my_form():
    username = request.args.get('username', '')
    if username:
        return render_template('status.html',
                               username=username,
                               sites=sites,
                               logos=logos,
                               host_backend=HOST_BACKEND,
                               port_backend=PORT_BACKEND,
                               protocol_backend=PROTOCOL_BACKEND)
    return render_template('form.html')

@app.route('/', methods=['POST'])
@cross_origin(origin='*')
def my_form_post():
    username = request.form['text']
    return render_template('status.html',
                           username=username,
                           sites=sites,
                           logos=logos,
                           host_backend=HOST_BACKEND,
                           port_backend=PORT_BACKEND,
                           protocol_backend=PROTOCOL_BACKEND)


if __name__ == '__main__':
    handler = logging.FileHandler('static/logs.log')
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] '
                                  '%(asctime)s %(message)s')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    if not (HOST_BACKEND and PORT_BACKEND):
        app.logger.error('Both HOST_BACKEND and PORT_BACKEND'
                         ' should be set before running')
        sys.exit(1)
    if not PORT_FRONTEND:
        app.logger.error('PORT_FRONTEND is not set')
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(PORT_FRONTEND))
