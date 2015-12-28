#Takes username as Input
#Needs the following dependencies :
# pip install requests[security]
# pip install termcolor

import requests
from termcolor import colored
username = raw_input("Enter the username : ")
f = "https://facebook.com/"+username
t = "https://twitter.com/"+username
i = "https://instagram.com/"+username

fr = requests.get(f)
tr = requests.get(t)
ir = requests.get(i)

def check(status_code):
	if(status_code == 404):
		print colored('Available', 'green')
	else: 
		print colored('Taken', 'red')


print f
check(fr.status_code)

print t
check(tr.status_code)

print i
check(ir.status_code)
