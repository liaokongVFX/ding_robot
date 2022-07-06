import hmac
import hashlib
import base64
from datetime import datetime
from datetime import timedelta

import config


def verify_sign(timestamp, sign):
    if not timestamp or not sign:
        return False

    current_timestamp = int((datetime.now() + timedelta(hours=1)).timestamp() * 1000)
    if current_timestamp < timestamp:
        return False

    app_secret = config.AppSecret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    new_sign = base64.b64encode(hmac_code).decode('utf-8')
    if new_sign != sign:
        return False

    return True
