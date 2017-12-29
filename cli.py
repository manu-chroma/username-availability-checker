import yaml
from username_api import check_username

patterns = yaml.load(open('websites.yml'))

sites = list(patterns['username_patterns'].keys())


def main():
    username = input('Enter the username : ')
    print('Checking username availability now...')

    for site in sites:
        res = check_username('{}.com'.format(site), username)
        if res['status'] == 404 or res['status'] == 301:
            print('Taken/Not Available on {}'.format(site))
        else:
            print('Taken on {}'.format(site))


if __name__ == '__main__':
    main()
