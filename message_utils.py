# -*- coding: utf-8 -*-

def make_text(text, at_user_ids=None, at_mobiles=None, at_all=False):
    data = {
        'at': {},
        'text': {
            'content': text
        },
        'msgtype': 'text'
    }
    if at_user_ids:
        data['at']['atUserIds'] = at_user_ids

    if at_mobiles:
        data['at']['atMobiles'] = at_mobiles

    if at_all:
        data['at']['isAtAll'] = True

    return data
