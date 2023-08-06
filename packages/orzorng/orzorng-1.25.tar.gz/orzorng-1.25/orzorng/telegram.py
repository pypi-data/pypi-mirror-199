# -*- coding: utf-8 -*-

from .network import request_api

class Telegram:
    api = ''

    def __init__(self, api=None):
        if api is not None:
            self.api = api

    def text(self, msg, chat_id='-448484122'):
        # print(self.api, 'send_tel', msg)
        request_api(self.api, 'tel', {
            'token': '1867591379:AAF33OrDpVm842wggRxi-TnKpP4lGPa1P3s',
            'chat_id': chat_id,
            'text': f'<code>{msg}</code>',
            'parse_mode': 'html',
        })

    def photo(self, photo_url, msg, chat_id='-448484122'):
        # print(self.api, 'send_photo', photo_url, msg)
        request_api(self.api, 'tel', {
            'type': 'sendPhoto',
            'token': '1867591379:AAF33OrDpVm842wggRxi-TnKpP4lGPa1P3s',
            'chat_id': chat_id,
            # 'chat_id': '1926915011',
            'photo': photo_url,
            'caption': f'{msg}',
            # 'parse_mode': 'html',
        })
        # print(res.json())
