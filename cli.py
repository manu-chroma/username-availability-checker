import requests
from username_api import check_username

sites = list(map(lambda x: '{}.com'.format(x), 
	"facebook twitter instagram github youtube soundcloud tumblr".split()))

def main():
	username = input("Enter the username : ")
	print('Checking username availability now...')

	for site in sites:
		res = check_username('{}.com'.format(site), username)
		if(res['status'] == 404 or res['status'] == 301):
			print("Taken/Not Available on {}".format(site))
		else:
			print("Taken on {}".format(site))
			
if __name__ == '__main__':
	main()
	