import json
import requests
from functools import partial


def send_wechat_msg(content, webhook_url):
    data = {"msgtype": "markdown", "markdown": {"content": content}}
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), verify=False)
    return r.text, r.status_code


def send_wechat_msg_custom(data, webhook_url):
    r = requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), verify=False)
    return r.text, r.status_code


get_default_report = lambda wechat_webhook: partial(send_wechat_msg, **{'webhook_url': wechat_webhook})
get_custom_report = lambda wechat_webhook: partial(send_wechat_msg_custom, **{'webhook_url': wechat_webhook})
