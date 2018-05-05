"""
Tests ontulily.floods.flood.py
"""
from unittest.mock import patch

from django.test import TestCase

from requests.exceptions import RetryError
from fake_useragent import UserAgent

from ontulily.floods.flood import get_request, requests_retry_session


class TestFlood(TestCase):
    """
    Test the methods in flood.py
    """
    def test_get_request(self):
        """
        Test that a request to a valid URL actually goes through
        """
        r = get_request(url="https://example.com")
        self.assertEquals(True, r['success'])
        self.assertEquals(200, r['response'].status_code)

    @patch('ontulily.floods.flood.requests_retry_session')
    def test_get_request_params(self, mocked):
        """
        Test that get_request passes the expected arguments
        """
        proxy = {'http': 'http:127.0.0.1'}
        params = {'foo': 'bar'}
        url = 'http://example.com'
        user_agent = UserAgent().chrome
        headers = {
            "Connection": "close",  # another way to cover tracks
            'User-Agent': str(user_agent)}

        get_request(url=url, user_agent=user_agent, proxy=proxy,
                    params=params)

        mocked().get.assert_called_with(
            url,
            proxies=proxy,
            params=params,
            headers=headers
        )

    def test_requests_retry_session_success(self):
        """
        Test that a valid URL can be accessed normally
        """
        r = requests_retry_session(retries=0,
                                   backoff_factor=0).get('http://example.com')
        self.assertEquals(200, r.status_code)

    def test_requests_retry_session_error(self):
        """
        Tests that an invalid URL will eventually fail
        """
        with self.assertRaises(RetryError):
            requests_retry_session(
                retries=0, backoff_factor=0).get(
                    'http://httpbin.org/status/500')
