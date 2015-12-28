from flask import Flask, request, render_template
from jinja2 import Template
import requests

app = Flask(__name__)

def check(status_code):
		if(status_code == 404):
			return 'Available'
		else: return 'Taken'

@app.route('/')
def my_form():
    return render_template("myform.html")

#def hi():
#	return "Enter your username : "


#@app.route('/<username>/')
#def user(username):

@app.route('/', methods=['POST'])
def my_form_post():
	username = request.form['text']
	f = "https://facebook.com/"+username
	t = "https://twitter.com/"+username
	i = "https://instagram.com/"+username
	fr = requests.get(f)
	tr = requests.get(t)
	ir = requests.get(i)
	x = check(fr.status_code)
	y = check(tr.status_code)
	z = check(ir.status_code)
	return render_template('world.html', username=username, fr=x, tr=y,ir=z )

if __name__ == "__main__":
	app.run()
