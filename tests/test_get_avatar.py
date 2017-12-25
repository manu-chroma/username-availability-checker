import unittest
import json
import requests as r
import yaml
import pytest
from parameterized import parameterized
import logging
import username_api
import os.path

data = yaml.load(open(os.path.join('tests', 'test_data.yml')))
websites = yaml.load(open('websites.yml'))


def load_test_cases(type):
	res = []
	for website in data:
		if website in ['behance', 'openhub', 'opensuse']:
			users = [None]
		elif type == 'with_avatar':
			if 'avatar_usernames' in data[website]:
				users = data[website]['avatar_usernames']
			else:
				users = data[website]['taken_usernames']
		else:
			users = data[website]['available_usernames']
		res.extend((website, user) for user in users)

	return res


def custom_name_func(testcase_func, param_num, param):
	return '%s_%s' % (
		testcase_func.__name__,
		parameterized.to_safe_name('_'.join(str(x) for x in param.args)),
	)


class TestGet_avatar(object):

	@parameterized.expand(load_test_cases('with_avatar'),
						  testcase_func_name=custom_name_func)
	def test_with_avatar(self, website, user):
		if not user:
			pytest.skip("website not supported")
		link = username_api.check_username(website, user)['avatar']
		response = r.get(link)
		assert(response.headers.get('content-type', '').startswith('image/') or
			   response.headers.get('content-type') == 'application/octet-stream')

	@parameterized.expand(load_test_cases('without_avatar'),
						  testcase_func_name=custom_name_func)
	def test_without_avatar(self, website, user):
		if not user:
			pytest.skip("website not supported")
		assert username_api.check_username(website, user)['avatar'] is None
