import os
import certifi; os.environ["SSL_CERT_FILE"] = certifi.where()
from twisted.internet.task import react
import treq
from termcolor import colored

username = raw_input("Enter the username : ")
sites = ["facebook", "twitter", "instagram", "github", "youtube", "soundcloud"]

def check(status_code):
	if(status_code == 404):
		print colored('Available', 'green')
	else: 
		print colored('Taken', 'red')

def done(response):
	check(response.code)
	reactor.stop

def yo(d):
	print d.code
	check(d.code)

def yolo(reactor,url):
	d = treq.head(url)
	d.addCallback(yo)
	return d

def main(reactor, *args):
    for i, val in enumerate(sites):
		link = "https://"+sites[i]+".com/"+username
		d = treq.head('http://github.com/gffdfdfd')
    	d.addCallback(yo)	
    	return d

react(main, [])

