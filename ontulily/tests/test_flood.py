"""
Tests ontulily.floods.flood.py
"""
from unittest.mock import patch, MagicMock
import requests_mock
from django.test import TestCase

from fake_useragent import UserAgent
from requests.exceptions import RetryError

from ontulily.floods.flood import (async_requests_retry_session,
                                   future_session_handler, package_request,
                                   quick_request_urls, request_url)


class TestFlood(TestCase):
    """
    Test the methods in flood.py
    """
    def test_package_request(self):
        """
        Test that a package_request resturns as we expect
        """
        user_agent = UserAgent().chrome
        data = dict(
            url="http://example.com",
            user_agent=user_agent,
            proxy={'http': 'http://127.0.0.1'},
            params={'foo': 'bar'},
            headers={'Connection': 'close', 'Foo': 'BAR'},
            method='POST',
            data={'test': True})
        expected = dict(
            url="http://example.com",
            proxies={'http': 'http://127.0.0.1'},
            params={'foo': 'bar'},
            headers={'Connection': 'close', 'Foo': 'BAR',
                     'User-Agent': user_agent},
            method='POST',
            data={'test': True})
        r = package_request(**data)
        self.assertDictEqual(expected, r)

    @patch('ontulily.floods.flood.async_requests_retry_session')
    def test_request_url(self, mocked):
        """
        Test that request_url works

        Ensure that request_url calls the `request` method on FutureSession
        """
        user_agent = UserAgent().chrome
        data = dict(
            url="http://example.com",
            user_agent=user_agent,
            proxy={'http': 'http://127.0.0.1'},
            params={'foo': 'bar'},
            method='POST',
            data={'test': True})
        expected = dict(
            url="http://example.com",
            proxies={'http': 'http://127.0.0.1'},
            params={'foo': 'bar'},
            headers={'Connection': 'close', 'User-Agent': user_agent},
            method='POST',
            data={'test': True})
        request_url(**data)
        mocked().request.assert_called_with(**expected)

    def test_async_requests_retry_session_success(self):
        """
        Test that a valid URL can be accessed normally using async
        """
        future = async_requests_retry_session(
            retries=0, backoff_factor=0).get('http://example.com')
        r = future.result()
        self.assertEquals(200, r.status_code)

    def test_async_requests_retry_session_error(self):
        """
        Tests that an invalid URL will eventually fail using async
        """
        with self.assertRaises(RetryError):
            future = async_requests_retry_session(
                retries=0, backoff_factor=0).get(
                    'http://httpbin.org/status/500')
            future.result()

    def test_future_session_handler(self):
        """
        Test future_session_handler
        """
        mocked = MagicMock()
        mocked.result.return_value = 'Noma sana'
        result = future_session_handler(mocked)
        self.assertTrue(result['success'])
        self.assertEquals('Noma sana', result['response'])

    @requests_mock.Mocker()
    def test_quick_request_urls(self, mocked):
        """
        Test quick_request_urls
        """
        mocked.get('http://example.com', text='mosh was here')
        results = quick_request_urls(urls=['http://example.com'])
        result = list(results)[0]
        self.assertTrue(result['success'])
        self.assertEquals(200, result['response'].status_code)
        self.assertEquals('mosh was here', result['response'].text)

    @requests_mock.Mocker()
    def test_quick_request_urls_error(self, mocked):
        """
        Test quick_request_urls handles errors correctly
        """
        mocked.get('http://example.com', exc=ConnectionError)
        mocked.get('http://httpbin.org/status/500', real_http=True)
        mocked.get('http://invalidurl', real_http=True)
        results = quick_request_urls(
            urls=['http://example.com', 'http://httpbin.org/status/500',
                  'http://invalidurl'])
        results = list(results)
        for result in results:
            self.assertFalse(result['success'])
