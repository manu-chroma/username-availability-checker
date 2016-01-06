from flask import Flask, jsonify
import requests
import json
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/check/<website>/<username>', methods=['GET'])
@cross_origin(origin='*')
def check_username(website,username):
	return jsonify({'status' : requests.head("http://"+website+"/"+username).status_code})

if __name__ == '__main__':
    app.run(debug=True)