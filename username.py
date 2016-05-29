#Takes username as Input
#Needs the following dependencies :
# pip install requests[security]
# pip install termcolor

import requests
from termcolor import colored

username = raw_input("Enter the username : ")
sites = "facebook twitter instagram github youtube soundcloud tumblr".split()


def check(status_code):
	if status_code == 404:
		print(colored('Available', 'green'))
	else: 
		print(colored('Taken', 'red'))


for site in sites:
	if site == 'tumblr':
		url = "https://{}.{}.com/".format(username, site)
	else:	
		url = "https://{}.com/{}".format(site, username)
	print(url)
	check(requests.get(url).status_code)










