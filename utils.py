import os
import hmac
import hashlib
import base64
from datetime import datetime
from datetime import timedelta
import importlib.util

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


def import_module(model_path):
    name = os.path.basename(model_path).rsplit('.', 1)[0]
    spec = importlib.util.spec_from_file_location(name, model_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def init_plugins():
    file_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')
    plugins = []
    for file_name in os.listdir(file_root):
        file_path = os.path.join(file_root, file_name)
        if not os.path.isfile(file_path):
            continue

        mod = import_module(os.path.join(file_root, file_name))
        if not hasattr(mod, 'register'):
            continue

        register_func = getattr(mod, 'register')
        plugins += register_func()

    return {x.keyword: x() for x in plugins}
