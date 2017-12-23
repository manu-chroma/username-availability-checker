import unittest
import json
import yaml
import string
import random
import pytest
import logging
import username_api
import os.path

data = yaml.load(open(os.path.join('tests', 'test_data.yml')))
websites = yaml.load(open('websites.yml'))

invalid_username = '$very%long{invalid}user(name)'

def generate_random_username(length, first_char_letter=False):
  return ''.join(generate_random_character(length, first_char_letter))

def generate_random_character(length, first_char_letter):
  for i in range(length):
    if first_char_letter and i == 0:
      yield random.choice(string.ascii_letters)
    else:
      yield random.choice(string.ascii_letters + string.digits)

def assert_response(app, website, user, status):
  expected = get_expected_response(website, user, status)
  actual = get_response(app, website, user)

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

class TestUsernameApi(object):
  @classmethod
  def setup_class(self):
    self.app = username_api.app.test_client()
    self.data = data

  @pytest.mark.parametrize('user', data['github']['taken_usernames'])
  def test_taken_github_username(self, user):
    assert_response(self.app, 'github', user, 200)

  @pytest.mark.parametrize('user', data['soundcloud']['taken_usernames'])
  def test_taken_soundcloud_username(self, user):
    assert_response(self.app, 'soundcloud', user, 200)

  @pytest.mark.parametrize('user', data['gitlab']['taken_usernames'])
  def test_taken_gitlab_username(self, user):
    assert_response(self.app, 'gitlab', user, 200)

  @pytest.mark.parametrize('user', data['tumblr']['taken_usernames'])
  def test_taken_tumblr_username(self, user):
    assert_response(self.app, 'tumblr', user, 200)

  @pytest.mark.parametrize('user', data['behance']['taken_usernames'])
  def test_taken_behance_username(self, user):
    assert_response(self.app, 'behance', user, 200)

  @pytest.mark.parametrize('user', data['pinterest']['taken_usernames'])
  def test_taken_pinterest_username(self, user):
    assert_response(self.app, 'pinterest', user, 200)

  @pytest.mark.parametrize('user', data['instagram']['taken_usernames'])
  def test_taken_instagram_username(self, user):
    assert_response(self.app, 'instagram', user, 200)

  @pytest.mark.parametrize('user', data['twitter']['taken_usernames'])
  def test_taken_twitter_username(self, user):
    assert_response(self.app, 'twitter', user, 200)

  @pytest.mark.parametrize('user', data['facebook']['taken_usernames'])
  def test_taken_facebook_username(self, user):
    assert_response(self.app, 'facebook', user, 200)

  # testing available usernames
  @pytest.mark.parametrize('user', data['github']['available_usernames'])
  def test_available_github_username(self, user):
    expected = get_expected_response('github', user, 404)
    actual = get_response(self.app, 'github', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(32)
      expected = get_expected_response('github', user, 404)
      actual = get_response(self.app, 'github', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['soundcloud']['available_usernames'])
  def test_available_soundcloud_username(self, user):
    expected = get_expected_response('soundcloud', user, 404)
    actual = get_response(self.app, 'soundcloud', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(25)
      expected = get_expected_response('soundcloud', user, 404)
      actual = get_response(self.app, 'soundcloud', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['gitlab']['available_usernames'])
  def test_available_gitlab_username(self, user):
    expected = get_expected_response('gitlab', user, 404)
    actual = get_response(self.app, 'gitlab', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(32)
      expected = get_expected_response('gitlab', user, 404)
      actual = get_response(self.app, 'gitlab', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['tumblr']['available_usernames'])
  def test_available_tumblr_username(self, user):
    expected = get_expected_response('tumblr', user, 404)
    actual = get_response(self.app, 'tumblr', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(15)
      expected = get_expected_response('tumblr', user, 404)
      actual = get_response(self.app, 'tumblr', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['behance']['available_usernames'])
  def test_available_behance_username(self, user):
    expected = get_expected_response('behance', user, 404)
    actual = get_response(self.app, 'behance', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(15)
      expected = get_expected_response('behance', user, 404)
      actual = get_response(self.app, 'behance', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['pinterest']['available_usernames'])
  def test_available_pinterest_username(self, user):
    expected = get_expected_response('pinterest', user, 404)
    actual = get_response(self.app, 'pinterest', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(15)
      expected = get_expected_response('pinterest', user, 404)
      actual = get_response(self.app, 'pinterest', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['instagram']['available_usernames'])
  def test_available_instagram_username(self, user):
    expected = get_expected_response('instagram', user, 404)
    actual = get_response(self.app, 'instagram', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(15)
      expected = get_expected_response('instagram', user, 404)
      actual = get_response(self.app, 'instagram', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['twitter']['available_usernames'])
  def test_available_twitter_username(self, user):
    expected = get_expected_response('twitter', user, 404)
    actual = get_response(self.app, 'twitter', user)

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(15)
      expected = get_expected_response('twitter', user, 404)
      actual = get_response(self.app, 'twitter', user)

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  @pytest.mark.parametrize('user', data['facebook']['available_usernames'])
  def test_available_facebook_username(self, user):
    expected = get_expected_response('facebook', user, 404)
    actual = get_response(self.app, 'facebook', user)

    # this is special to facebook checking,
    # and 'profile' field is only useful for
    # frontend purposes. Skipping here.
    del actual['profile']

    message = None
    if expected != actual:
      message = 'The provided available username ({}) returned 200'.format(user)

      user = generate_random_username(25)
      expected = get_expected_response('facebook', user, 404)
      actual = get_response(self.app, 'facebook', user)

      del actual['profile']

      if expected != actual:
        message += ' and the random username ({}) returned 200'.format(user)
      else:
        message += ' but {} is still available'.format(user)

    if message is not None:
      logging.getLogger().warn(message)

    assert expected == actual

  # Check formatting of usernames
  def test_github_format_checking(self):
    resp = self.app.get('/check/github/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://github.com/{}'.format(invalid_username)
    } == json_resp

  def test_soundcloud_format_checking(self):
    resp = self.app.get('/check/soundcloud/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://soundcloud.com/{}'.format(invalid_username)
    } == json_resp

  def test_gitlab_format_checking(self):
    resp = self.app.get('/check/gitlab/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://gitlab.com/{}'.format(invalid_username)
    } == json_resp

  def test_tumblr_format_checking(self):
    resp = self.app.get('/check/tumblr/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://{}.tumblr.com'.format(invalid_username)
    } == json_resp

  def test_behance_format_checking(self):
    resp = self.app.get('/check/behance/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://behance.net/{}'.format(invalid_username)
    } == json_resp

  def test_pinterest_format_checking(self):
    resp = self.app.get('/check/pinterest/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://in.pinterest.com/{}'.format(invalid_username)
    } == json_resp

  def test_instagram_format_checking(self):
    resp = self.app.get('/check/instagram/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://instagram.com/{}'.format(invalid_username)
    } == json_resp

  def test_twitter_format_checking(self):
    resp = self.app.get('/check/twitter/{}'.format(invalid_username))
    json_resp = json.loads(resp.get_data().decode())
    assert {
      'possible': False,
      'url': 'https://twitter.com/{}'.format(invalid_username)
    } == json_resp

  def test_facebook_format_checking(self):
    invalid_username_facebook = ['hello..world', 'hell...', 'manvendra.com']

    for invalid_username in invalid_username_facebook:
      resp = self.app.get('/check/facebook/{}'.format(invalid_username))
      json_resp = json.loads(resp.get_data().decode())
      assert {
        'possible': False,
        'url': 'https://mbasic.facebook.com/{}'.format(invalid_username)
      } == json_resp
