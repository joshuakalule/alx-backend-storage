#!/usr/bin/env python3
"""Uses requests module to obtain the HTML content of a particular URL"""

import redis
import requests

_redis = redis.Redis()


def get_page(url: str) -> str:
    """Returns html text of url"""

    html = _redis.get(url)
    if html:
        # track times url is accessed
        _redis.incr(f"count:{url}")
        return str(html)

    html = requests.get(url).content.decode('utf-8')

    # cache result
    _redis.set(url, html, ex=10)
    return str(html)
