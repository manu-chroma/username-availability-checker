#Takes username as Input
#Needs the following dependencies :
# pip install requests[security]
# pip install termcolor

import requests
from termcolor import colored

username = raw_input("Enter the username : ")
sites = ["facebook", "twitter", "instagram", "github", "youtube", "soundcloud", "tumblr"]

def check(status_code):
	if(status_code == 404):
		print colored('Available', 'green')
	else: 
		print colored('Taken', 'red')


for i, val in enumerate(sites):
	if(sites[i] == 'tumblr'):
		a = requests.get("https://"+username+'.'+sites[i]+".com/") 
		print "https://"+username+'.'+sites[i]+".com/"
	else:	
		a = requests.get("https://"+sites[i]+".com/"+username)
		print "https://"+sites[i]+".com/"+username
	check(a.status_code)











