from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
import requests

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

def check_username(website, username):
	if website == 'tumblr.com':
		url = 'https://{}.{}'.format(username, website)
	else:
		url = 'http://{}/{}'.format(website, username)
	
	return {'status' : requests.get(url).status_code}

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