import json
import logging
import os.path
import random
import string

from parameterized import parameterized
import pytest
import yaml

import username_api

data = yaml.load(open(os.path.join('tests', 'test_data.yml')))
websites = yaml.load(open('websites.yml'))

invalid_username = '$very%long{invalid}user(name)'

def generate_random_username(website, length):
  first_char_letter = False
  if website == 'openhub':
    first_char_letter = True
  return ''.join(generate_random_character(length,
    first_char_letter=first_char_letter))

def generate_random_character(length, first_char_letter):
  for i in range(length):
    if first_char_letter and i == 0:
      yield random.choice(string.ascii_letters)
    else:
      yield random.choice(string.ascii_letters + string.digits)

def assert_response(app, website, user, status):
  expected = get_expected_response(website, user, status)
  actual = get_response(app, website, user)
  assert actual == expected

def get_response(app, website, user):
  resp = app.get('/check/{}/{}'.format(website, user))
  return json.loads(resp.get_data().decode())

def get_expected_response(website, user, status):
  return {
    'possible': True,
    'status': status,
    'url': username_api.get_profile_url(website, user),
    'avatar': username_api.get_avatar(website, user) if status == 200
              else None
  }

def load_availability_test_cases(status):
  res = []
  for website in data:
    if status == 'available_username':
      usernames = data[website]['available_usernames']
    if status == 'taken_username':
      usernames = data[website]['taken_usernames']
    res.extend((website, user) for user in usernames)

  return res

def load_format_checking_cases():
  res = []
  for website in data:
    usernames = data[website]['invalid_usernames']
    res.extend((website, user) for user in usernames)

  return res

def custom_name_func(testcase_func, param_num, param):
  return '%s_%s' % (
    testcase_func.__name__,
    parameterized.to_safe_name('_'.join(str(x) for x in param.args)),
  )

class TestUsernameApi(object):
  @classmethod
  def setup_class(self):
    self.app = username_api.app.test_client()
    self.websites = websites

  @parameterized.expand(load_availability_test_cases('available_username'),
      testcase_func_name=custom_name_func)
  def test_available_username(self, website, user):
    expected = get_expected_response(website, user, 404)
    actual = get_response(self.app, website, user)

    # this is special to facebook checking,
    # and 'profile' field is only useful for
    # frontend purposes. Skipping here.
    if website == 'facebook':
      del actual['profile']

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)
      username_pattern = self.websites['username_patterns'][website]
      username_length = 15

      user = generate_random_username(website, username_length)
      expected = get_expected_response(website, user, 404)
      actual = get_response(self.app, website, user)

      if website == 'facebook':
        del actual['profile']

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @parameterized.expand(load_availability_test_cases('taken_username'),
      testcase_func_name=custom_name_func)
  def test_taken_username(self, website, user):
    assert_response(self.app, website, user, 200)

  @parameterized.expand(load_format_checking_cases(),
      testcase_func_name=custom_name_func)
  def test_format_checking(self, website, username):
    resp = self.app.get('/check/{w}/{u}'.format(w=website, u=username))
    json_resp = json.loads(resp.get_data().decode())
    url = username_api.get_profile_url(website, username)
    assert {
      'possible': False,
      'url': url
    } == json_resp
