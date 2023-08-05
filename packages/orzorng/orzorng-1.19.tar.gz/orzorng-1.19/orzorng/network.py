# -*- coding: utf-8 -*-

import os
import json
import time
import random
import requests

def random_dict(dicts):
    dict_key_ls = list(dicts.keys())
    random.shuffle(dict_key_ls)
    new_dict = {}
    for key in dict_key_ls:
        new_dict[key] = dicts.get(key)
    return new_dict

requests_api_err_num = 0


def request_api(local_sql, action, data, timeout=120, req_err_func=None):
    global requests_api_err_num
    try:
        res = requests.post(local_sql + '&_=' + str(int(time.time())), random_dict(dict({'action': action}, **data)),
                            timeout=timeout)
        # print('ok request_api', action, res.text)

        if res.status_code == 200:
            json.loads(res.text)
        else:
            raise Exception(f'状态码不对 {res.status_code}')

        print('ok request_api', action)
        requests_api_err_num = 0
        return res
    except Exception as get_err:
        print('err request_api', local_sql, action, get_err)
        time.sleep(1)
        requests_api_err_num += 1

        if requests_api_err_num > 3:
            if req_err_func != None:
                req_err_func()
                requests_api_err_num = 0

        return request_api(local_sql, action, data, timeout, req_err_func)


class ChangeIp:
    changeIpTime = 0
    changeIpInterval = 20

    vpsUsername = ''
    vpsPassword = ''

    # 成功钩子函数
    dialSuccessFunc = None

    def __init__(self, dial_success_func=None):
        if os.name == "nt":
            if os.path.exists('宽带连接.txt'):
                with open('宽带连接.txt', 'r', encoding='utf-8') as kd_f:
                    kd_str = kd_f.read().strip()
                    if kd_str:
                        self.vpsUsername, self.vpsPassword = kd_str.split('|')

        if dial_success_func is not None:
            self.dialSuccessFunc = dial_success_func

    def dial(self):
        try:

            change_ip_diff = int(time.time()) - self.changeIpTime
            if change_ip_diff < self.changeIpInterval:
                print('切换 ip 间隔过小 sleep ', self.changeIpInterval - change_ip_diff)
                time.sleep(self.changeIpInterval - change_ip_diff)

            if os.name == "nt":
                os.system("rasdial %s /d" % ('宽带连接'))
                os.system("rasdial %s %s %s" % ('宽带连接', self.vpsUsername, self.vpsPassword))
            else:
                os.system('pppoe-stop')
                os.system('pppoe-start')

            self.changeIpTime = int(time.time())
            print('更換ip成功')

            # 成功钩子
            if self.dialSuccessFunc is not None:
                self.dialSuccessFunc()

            return True

        except Exception as e:
            print('更换ip失败: ', e)

        time.sleep(1)
        return self.dial()
