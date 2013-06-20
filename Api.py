__author__ = 'rast'

import json
import urllib2
from urllib import urlencode
import re
from time import sleep

_counter = 0
_max_calls = 5

def auth(args, access_rights):
    """Interact with user to get access_token"""

    url = "https://oauth.vk.com/oauth/authorize?" + \
          "redirect_uri=https://oauth.vk.com/blank.html&response_type=token&" + \
          "client_id=%s&scope=%s&display=wap" % (args.app_id, ",".join(access_rights))

    print("Please open this url:\n\n\t{}\n".format(url))
    raw_url = raw_input("Grant access to your acc and copy resulting URL here: ")
    res = re.search('access_token=([0-9A-Fa-f]+)', raw_url, re.I)
    if res is not None:
        return res.groups()[0]
    else:
        return None

def call_api(method, params, token):
    global _counter
    if _counter == _max_calls:
        sleep(1)
        _counter = 0
    else:
        _counter += 1
    if isinstance(params, list):
        params_list = [kv for kv in params]
    elif isinstance(params, dict):
        params_list = params.items()
    else:
        params_list = [params]
    params_list.append(("access_token", token))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params_list))
    json_stuff = urllib2.urlopen(url).read()
    result = json.loads(json_stuff)
    if u'error' in result.keys():
        raise RuntimeError("API call resulted in error ({}): {}".format(result[u'error'][u'error_code'],
                                                                        result[u'error'][u'error_msg']))

    if not u'response' in result.keys():
        raise RuntimeError("API call result has no response")
    else:
        return (result[u'response'], json_stuff)