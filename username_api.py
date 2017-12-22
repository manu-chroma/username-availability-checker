from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
import requests as r
from bs4 import BeautifulSoup

import os
import sys
import re
import yaml

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

patterns = yaml.load(open('websites.yml'))

def get_profile_url(website, username):
	return patterns['urls'].get(website, 'https://{w}.com/{u}').format(
		w=website,
		u=username
	)

def get_avatar(website, username):
	data = patterns['avatar'][website]

	if not data:
		return None

	url = get_profile_url(website, username)
	if 'url' in data:
		url = data['url'].format(u=username)

	response = r.get(url)
	if response.status_code == 404:
		return None

	if data == 'opengraph':
		# Look in metadata for image.
		soup = BeautifulSoup(response.text, 'html.parser')
		result = [item.attrs['content'] for item in soup('meta')
				  if item.has_attr('property') and
				  item.attrs['property'].lower() == 'og:image']
		if not result or not result[0]:
			return None
		result = result[0]
	elif 'key' in data:
		# Searches for "`key`": "`link`"
		regex = re.compile('[\'\"]' + re.escape(data['key']) +
						   '[\'\"]:(\s)?[\'\"](?P<link>[^\s]+)[\'\"]')
		result = re.search(regex, response.text)
		if not result:
			return None
		result = result.group('link')
	elif response.headers.get('content-type', '').startswith('image/'):
		return url
	else:
		return None

	# Fix relative links
	if result[0] == '/':
		base_url = get_profile_url(website, '')
		result = base_url + result
	return result

def check_username(website, username):
	url = get_profile_url(website, username)
	possible = check_format(website, username)

	if not possible:
		return {
			'url': url,
			'possible': possible,
		}

	if website in ['pinterest', 'gitlab', 'opensuse']:
		res  = r.get(url)
		if bytes(username, encoding='utf-8') in res.content:
			code = 200
		if bytes('About me', encoding='utf-8') in res.content:
			code = 200
		else:
			code = 404

		return {
			'status': code,
			'url': url,
			'avatar': get_avatar(website, username)
			'possible': possible,
		}

	elif website == 'facebook':
		res = r.get(url)
		code = res.status_code
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
		}

	else:
		return {
			'status': r.get(url).status_code,
			'url': url,
			'avatar': get_avatar(website, username),
			'possible': possible,
		}

def check_format(website, username):
	"""Check the format of a username depending on the website"""

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
		username = username.replace(".", "")

		if len(username) <= 5:
			return False

	if matches is not None:
		return True
	else:
		return False

# API endpoints
@app.route('/')
@cross_origin(origin='*')
def hello():
	return "Hello world! The app seems to be working!"

@app.route('/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check(website, username):
	return jsonify(check_username(website, username))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8521)
