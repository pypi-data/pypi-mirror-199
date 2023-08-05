# -*- coding: utf-8 -*-

# listTemp 为列表 平分后每份列表的的个数n
def list_block(list_temp, n):
    for i in range(0, len(list_temp), n):
        yield list_temp[i:i + n]


