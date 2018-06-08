import collections
import json
import os.path

from parameterized import parameterized
import exrex
import pytest
import yaml

import username_api

data = yaml.load(open(os.path.join('tests', 'test_data.yml')))
websites = yaml.load(open('websites.yml'))

AvailabilityTestCase = collections.namedtuple(
    'AvailabilityTestCase',
    'website username')


@pytest.fixture(params=data.keys())
def random_available_min_username(request):
    """
    Pytest fixture for loading test case.

    This contains available username of minimum length.
    """
    return AvailabilityTestCase(
        request.param,
        generate_random_valid_username(
            request.param,
            websites['username_patterns'][request.param]['available_min_length']))


def generate_random_username(website, length):
    """
    Generate random username for specific website and length.

    Note that the result could be invalid username.
    """
    username_pattern = websites['username_patterns'][website]
    # This range(100) is a temporary workaround to avoid looping forever
    # which is caused by generating random values.
    for _ in range(100):
        yield exrex.getone('[{chars}]{{{len}}}'.format(
            chars=username_pattern['characters'],
            len=length))


def generate_random_valid_username(website, length):
    """
    Generate valid random username for specific website and length.

    generate_random_valid_username works like generate_random_username
    but it only returns valid username.
    It raise Exception if it cannot generate valid username
    """
    for random_username in generate_random_username(website, length):
        if username_api.check_format(website, random_username):
            return random_username
    raise Exception('Cannot generate valid username for username for {} of length {}',
                    website, length)


def assert_response(app, website, user, status):
    expected = get_expected_response(website, user, status)
    actual = get_response(app, website, user)
    assert actual == expected


def get_response(app, website, user):
    resp_bytes = app.get('/check/{}/{}'.format(website, user))
    resp_dict = json.loads(resp_bytes.get_data().decode())
    # this is special to facebook checking,
    # and 'profile' field is only useful for
    # frontend purposes. Skipping here.
    if website == 'facebook':
        del resp_dict['profile']

    return resp_dict


def get_expected_response(website, user, status):
    return {
        'possible': True,
        'usable': True,
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
        if status == 'random_max_username':
            usernames = [
                generate_random_valid_username(
                    website,
                    websites['username_patterns'][website]['max_length'])
                ]
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
        assert_response(self.app, website, user, 404)

    @parameterized.expand(load_availability_test_cases('random_max_username'),
                          testcase_func_name=custom_name_func)
    def test_random_max_username(self, website, user):
        assert_response(self.app, website, user, 404)

    @pytest.mark.flaky(reruns=10)
    def test_random_available_min_username(self, random_available_min_username):
        assert_response(self.app,
                        random_available_min_username.website,
                        random_available_min_username.username,
                        404)

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
            'usable': True,
            'url': url
        } == json_resp
