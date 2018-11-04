import logging
import os
import sys
import json

from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask.ext.cors import CORS, cross_origin
import yaml

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
signup = ' '.join(list(patterns['signup'].keys()))


@app.route('/', methods=['GET'])
@cross_origin()
def my_form():
    username = request.args.get('username', '')
    if username:
        return render_template('status.html',
                               username=username,
                               sites=sites,
                               signup=signup,
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
                           signup=signup,
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
