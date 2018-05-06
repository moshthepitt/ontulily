"""
ontulily HTTP Flood module

See: https://github.com/moshthepitt/ontulily/blob/master/docs/flood.md
"""
import requests
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from requests.packages.urllib3.util.retry import Retry
from requests_futures.sessions import FuturesSession

from ontulily.settings import (MAX_WORKERS, REQUESTS_BACKOFF, REQUESTS_RETRIES,
                               REQUESTS_STATUS_FORCELIST)

USERAGENT = UserAgent()


def get_request(url: str,
                user_agent: str=None,
                proxy: dict=None,
                params: dict=None,
                retries: int=REQUESTS_RETRIES,
                backoff_factor: float=REQUESTS_BACKOFF,
                status_forcelist: set=REQUESTS_STATUS_FORCELIST):
    """
    Sends a GET request to a URL
    """
    if user_agent is None:
        user_agent = USERAGENT.random

    headers = {
        "Connection": "close",  # another way to cover tracks
        'User-Agent': str(user_agent)}

    result = {'success': False}

    try:
        r = requests_retry_session(
            retries=retries, backoff_factor=backoff_factor,
            status_forcelist=status_forcelist).get(
                url,
                proxies=proxy,
                params=params,
                headers=headers
            )
    except RetryError as e:
        result['error'] = e
    except ConnectionError as e:
        result['error'] = e
    else:
        result['success'] = True
        result['response'] = r
    finally:
        return result


def requests_retry_session(retries: int=REQUESTS_RETRIES,
                           backoff_factor: float=REQUESTS_BACKOFF,
                           status_forcelist: set=REQUESTS_STATUS_FORCELIST,
                           session: object=None):
    """
    A wrapper around requests to enable retrying

    See: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    """
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


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
