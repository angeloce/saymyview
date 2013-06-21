#coding:utf-8

import requests


class BrowserAgent:
    CHROME_DESKTOP = "User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36"
    CHROME_MOBILE = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"

    IE7 = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
    IE9 = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"

    IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
    IPAD = "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"




def request(method, url, **kwargs):

    default_kwargs = {
        "headers": {
            "User-Agent": BrowserAgent.CHROME_DESKTOP
        }
    }

    for key in default_kwargs:
        if key in kwargs:
            pass
