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

print f
if(fr.status_code == 404):
	print colored('Available', 'green')
else: print colored('Taken', 'red')

print t
if(tr.status_code == 404):
	print colored('Available', 'green')
else: print colored('Taken', 'red')

print i
if(ir.status_code == 404):
	print colored('Available', 'green')
else: print colored('Taken', 'red')
