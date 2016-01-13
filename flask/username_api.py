from flask import Flask, jsonify
import requests
import json
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin(origin='*')
def hello():
	return "hello world"

@app.route('/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check_username(website,username):
	if(website == 'tumblr.com'):
		return jsonify({'status' : requests.get("https://"+username+"."+website).status_code})
		
	return jsonify({'status' : requests.get("http://"+website+"/"+username).status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8521)