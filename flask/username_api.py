from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
#import json
import requests

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin(origin='*')
def hello():
	return "hello world"

@app.route('/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check_username(website, username):
	if website == 'tumblr.com':
		url = 'https://{}.{}'.format(username, website)
	else:
		url = 'http://{}/{}'.format(website, username)
	return jsonify({'status' : requests.get(url).status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8521)
