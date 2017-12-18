from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
import requests as r

import sys
import re
import yaml

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

patterns = yaml.load(open('websites.yml'))

def check_username(website, username):
	url = patterns['urls'].get(website, 'https://{w}.com/{u}').format(
		w=website,
		u=username
	)

	possible = check_format(website, username)

	if not possible:
		return {
			'url': url,
			'possible': possible,
		}

	if website in ['pinterest', 'gitlab']:
		res  = r.get(url)
		code = 200 if bytes(username, encoding='utf-8') in res.content \
			else 404

		return {
			'status': code,
			'url': url,
			'possible': possible,
		}
	else:
		return {
			'status': r.get(url).status_code,
			'url': url,
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