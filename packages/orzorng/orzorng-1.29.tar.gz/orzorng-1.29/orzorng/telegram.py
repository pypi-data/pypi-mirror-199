# -*- coding: utf-8 -*-

from .network import request_api


class Telegram:
    api = ''
    chat_id = ''
    token = ''

    def __init__(self, api=None, chat_id=None, token=None):
        if api is not None:
            self.api = api

        if chat_id is not None:
            self.chat_id = chat_id

        if token is not None:
            self.token = token

    # -448484122  网站请求异常
    # 1926915011  工作号

    def text(self, msg, chat_id=None, token=None):
        if chat_id is None:
            chat_id = self.chat_id

        if token is None:
            token = self.token

        # print(self.api, {
        #     'token': token,
        #     'chat_id': chat_id,
        #     'text': f'<code>{msg}</code>',
        #     'parse_mode': 'html',
        # })
        # print(self.api, 'send_tel', msg)
        request_api(self.api, 'tel', {
            'token': token,
            'chat_id': chat_id,
            'text': f'<code>{msg}</code>',
            'parse_mode': 'html',
        })

    def photo(self, photo_url, msg, chat_id=None, token=None):
        if chat_id is None:
            chat_id = self.chat_id

        if token is None:
            token = self.token

        # print(self.api, 'send_photo', photo_url, msg)
        request_api(self.api, 'tel', {
            'type': 'sendPhoto',
            'token': token,
            'chat_id': chat_id,
            'photo': photo_url,
            'caption': f'{msg}',
            # 'parse_mode': 'html',
        })
        # print(res.json())
