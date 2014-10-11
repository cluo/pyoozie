#!/usr/bin/env python
#!-*- coding:utf-8 -*-

start_node = {
    'act_type':'start',
    'name':'start',
    'to': 'first_decision',
}


decision_node = {
    'act_type':'decision',
    'name':'first_decision',
    'to': 'end',
    'decisions':{'default':'end',
                 'file_exists':['/user/brian/myroot/_SUCCESS', 'pig1'], #如果文件myroot/_SUCCESS存在，执行pig1 action
                 'file_not_exists':['/user/brian/myroot/_SUCCESS', 'end'], #如果文件myroot/_SUCCESS不存在，执行kill action
                 #以类似的方式，实现更多的decision功能，具体请参考DecisionAction实现。
               },
}


pig1_node = {
    'act_type':'pig',
    'name':'pig1',
    'pig_dir':'/home/brian/python-test/pyoozie/pigs',#pig文件所在目录
    'pig_file': 'fork1.pig',#pig文件名
    'to':'end',
}


end_node = {
    'act_type':'end',
    'name':'end',
}


nodes = [start_node, decision_node, pig1_node, end_node]
