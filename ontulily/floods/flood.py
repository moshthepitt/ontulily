"""
ontulily HTTP Flood module

See: https://github.com/moshthepitt/ontulily/blob/master/docs/flood.md
"""
import concurrent.futures
from typing import List

from django.conf import settings

from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from requests.packages.urllib3.util.retry import Retry
from requests_futures.sessions import FuturesSession

USERAGENT = UserAgent()

MAX_WORKERS = settings.MAX_WORKERS
REQUESTS_BACKOFF = settings.REQUESTS_BACKOFF
REQUESTS_RETRIES = settings.REQUESTS_RETRIES
REQUESTS_STATUS_FORCELIST = settings.REQUESTS_STATUS_FORCELIST


def package_request(url: str, user_agent: str=None, proxy: dict=None,
                    params: dict=None, headers: dict=None, method: str='GET',
                    data: dict=None):
    """
    Prepares a GET request
    """

    if user_agent is None:
        user_agent = USERAGENT.random

    if headers is None:
        headers = {
            "Connection": "close",  # another way to cover tracks
            'User-Agent': str(user_agent)}
    else:
        headers['User-Agent'] = str(user_agent)
    return dict(
        method=method,
        url=url,
        params=params,
        data=data,
        headers=headers,
        proxies=proxy
    )


def async_requests_retry_session(
        retries: int=REQUESTS_RETRIES, backoff_factor: float=REQUESTS_BACKOFF,
        status_forcelist: set=REQUESTS_STATUS_FORCELIST, session: object=None,
        max_workers: int=MAX_WORKERS):
    """
    A wrapper around requests to enable retrying that uses async requests
    """
    session = session or FuturesSession(max_workers=MAX_WORKERS)
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def request_url(
            url: str, user_agent: str=None, proxy: dict=None,
            params: dict=None, headers: dict=None, method: str='GET',
            data: dict=None, retries: int=REQUESTS_RETRIES,
            backoff_factor: float=REQUESTS_BACKOFF,
            status_forcelist: set=REQUESTS_STATUS_FORCELIST,
            session: object=None, max_workers: int=MAX_WORKERS):
    """
    Sends a request to a url, returns a FutureSession object
    """
    the_request = package_request(
        url=url,
        user_agent=user_agent,
        proxy=proxy,
        params=params,
        headers=headers,
        method=method,
        data=data
    )
    the_session = async_requests_retry_session(
        retries=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        session=session,
        max_workers=max_workers
    )
    return the_session.request(**the_request)


def future_session_handler(future_session: object):
    """
    Handler for future session objects
    """
    result = {'success': False}

    try:
        result['response'] = future_session.result()
    except RetryError as e:
        result['error'] = e
    except ConnectionError as e:
        result['error'] = e
    else:
        result['success'] = True
    finally:
        return result


def quick_request_urls(
        urls: List[str], proxy: dict=None, params: dict=None, data: dict=None,
        method: str='GET'):
    """
    Shortcut to send the same request to a bunch of urls
    """
    futures = (
        request_url(
            method=method, url=url, proxy=proxy, params=params, data=data) for
        url in urls)
    for future_result in concurrent.futures.as_completed(futures):
        yield future_session_handler(future_result)
