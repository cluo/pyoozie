#!/usr/bin/env python 
#!-*- coding:utf-8 -*-

start_node = {
    'act_type':'start',
    'name':'start',
    'to': 'first_pig',
}


pig_node = {
    'act_type':'pig',
    'name':'first_pig',
    'to': 'end',
    'pig_dir':'/home/brian/python-test/pyoozie/pigs',#pig文件所在目录
    'pig_file': 'myroot.pig',#pig文件名
}


end_node = {
    'act_type':'end',
    'name':'end',
}


nodes = [start_node, pig_node, end_node]
