#!/usr/bin/env python 
#!-*- coding:utf-8 -*-

start_node = {
    'act_type':'start',
    'name':'start',
    'to': 'first_fork',
}


fork_node = {
    'act_type':'fork',
    'name':'first_fork',
    'to': 'end',
    'fork_nodes':['pig1', 'pig2'],
}


pig1_node = {
    'act_type':'pig',
    'name':'pig1',
    'pig_dir':'/home/brian/python-test/pyoozie/pigs',#pig文件所在目录
    'pig_file': 'fork1.pig',#pig文件名
}


pig2_node = {
    'act_type':'pig',
    'name':'pig2',
    'pig_dir':'/home/brian/python-test/pyoozie/pigs',#pig文件所在目录
    'pig_file': 'fork2.pig',#pig文件名
}


end_node = {
    'act_type':'end',
    'name':'end',
}


nodes = [start_node, fork_node, pig1_node, pig2_node, end_node]
