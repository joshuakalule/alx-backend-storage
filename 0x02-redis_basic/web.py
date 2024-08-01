#!/usr/bin/env python3
"""Uses requests module to obtain the HTML content of a particular URL"""

import redis
import requests

_redis = redis.Redis()

def get_page(url: str) -> str:
    """Returns html text of url"""

    # check in cache
    if _redis.exists(url):
        return _redis.get(url)

    # track times url is accessed
    _redis.incr(f"count:{url}")

    html = requests.get(url).content.decode('utf-8')

    # cache result
    _redis.set(url, html, ex=10)
    print("type: ", type(html))
    return str(html)
