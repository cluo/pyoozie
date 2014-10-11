#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import time
import subprocess

from Queue import Queue
from threading import Thread

from utils import *

class Action(object):
    act_type = 'action'

    def __init__(self, node):
        self.node = node

    def get_name(self):
        return self.node['name']

    def to(self):
        try:
            return self.node['to']
        except:
            return ''

    def __repr__(self):
        return "Action: ActionType = %s, node = %s" %(self.act_type, self.node)


"""
Control Flow Action
"""
class StartAction(Action):
    """
    start action，指明工作流的第一个action是什么。
    """
    act_type = 'start'


class EndAction(Action):
    """
    执行到end action，表示工作流成功。至此，一切action都应该结束了，如果有没结束的action，要kill掉。
    """
    act_type = 'end'


class DecisionAction(Action):
    act_type = 'decision'

    def to(self):
        ret = ''
        for i in self.node['decisions'].keys():
            if i == 'file_exists':
                if is_file_dir_exists(self.node['decisions'][i][0]):
                    ret = self.node['decisions'][i][-1]
                    break
            elif i == 'file_not_exists':
                if not is_file_dir_exists(self.node['decisions'][i][0]):
                    ret = self.node['decisions'][i][-1]
                    break
            else:
                pass

        if ret == '':
            if 'default' in self.node['decisions'].keys():
                ret = self.node['decisions']['default']
            else:
                ret = 'end'

        return ret
 

class ActionThread(Thread):
    """
    在ForkAction需要多线程执行若干个Action，ActionThread提供线程执行功能。用Queue传递线程执行结果。
    """
    def set(self, action, msgq):
        self.action = action
        self.msgq = msgq
    
    def run(self):
        ret = self.action.run()
        self.msgq.put("%s:%s" %(self.action.get_name(), ret))


class ForkAction(Action):
    act_type = 'fork'

    def set_fork_actions(self, forked_actions):
        self.forked_actions = forked_actions

    def run(self):
        """
        获取fork内包含的若干个action，在新线程执行它们，然后返回结果。
        """
        ret = 0
        msgq = Queue(100)
        num = 0
        for i in self.forked_actions:
            x = ActionThread()
            x.set(i, msgq)
            x.start()
            num += 1

        while num > 0:
            time.sleep(1)
            name,rret = msgq.get().split(':')
            num -= 1
            rret = int(rret)
            if not rret == 0:
                ret = 3
        return ret


"""
Processing Action
"""
class PigAction(Action):
    """
    执行一个pig script。
    """
    act_type = 'pig'

    def run(self):
        cmd = subprocess.Popen(['pig', '-x', 'mapreduce', 
                                os.path.join(self.node['pig_dir'], self.node['pig_file'])], 
                                stdout=subprocess.PIPE)
        ret = cmd.wait()
        return ret


class MRAction(Action):
    """
    执行一个Map-Reduce作业
    """
    act_type = 'mr'

    def run(self):
        pass


class FsAction(Action):
    act_type = 'fs'


class SshAction(Action):
    act_type = 'ssh'


class EmailAction(Action):
    act_type = 'email'


"""
Work life manager
"""
class ActionKeeper:
    """
    存储所有的nodes。根据nodes生成Actions。检查dag是否存在cycle。检查Action的资源是否存在。检查执行链是否合理。检查是否有不能执行的Actions。
    """
    def __init__(self, nodes):
        self.nodes = nodes
        self.name_actions = {}
        for i in self.nodes:
            if i['act_type'] == 'start':
                ii = StartAction(i)
            elif i['act_type'] == 'end':
                ii = EndAction(i)
            elif i['act_type'] == 'pig':
                ii = PigAction(i)
            elif i['act_type'] == 'fork':
                ii = ForkAction(i)
            elif i['act_type'] == 'decision':
                ii = DecisionAction(i)
            elif i['act_type'] == 'ssh':
                ii = SshAction(i)
            elif i['act_type'] == 'email':
                ii = EmailAction(i)
            elif i['act_type'] == 'mr':
                ii = MRAction(i)
            elif i['act_type'] == 'fs':
                ii = FsAction(i)
            self.name_actions[i['name']] = ii

    def __repr__(self):
        s = ""
        for i in self.name_actions:
            s += "    %s,\n" % i
        return "ActionKeeper, actions = [\n%s]" % s

    def check_actions(self):
        self.check_cycle()
        self.check_resouce()

    def get_action(self, name):
        try:
            return self.name_actions[name]
        except:
            return None

    def check_cycle(self):
        #end节点可以被多次访问，其他节点都只能被访问一次，如果被访问多次，就存在cyle。
        colors = {}
        for i in self.name_actions.keys():
            colors[i] = 'white'
        def recurse_check(colors, name_actions, name):
            act = name_actions[name]
            if colors[name] == 'white':
                colors[name] = 'black'
            else:#'black'
                if name == 'end':
                    pass
                else:
                    raise Exception, "Action %s found cycle" % (name)

            if act.act_type == 'decision':
                for i in act.node['decisions'].keys():
                    if i == 'default': 
                        continue
                    recurse_check(colors, name_actions, act.node['decisions'][i][-1])
            elif act.act_type == 'fork':
                #删除fork的内的action，它们不需要检查
                for i in act.node['fork_nodes']:
                    colors.pop(i)
                to_name = act.to()
                if to_name == '':
                    pass
                else:
                    recurse_check(colors, name_actions, to_name)
            else:
                to_name = act.to()
                if to_name == '':
                    pass
                else:
                    recurse_check(colors, name_actions, to_name)

    def check_resouce(self):
        pass


class WorkFlowJob:
    def __init__(self, ak):
        self.ak = ak

    def start(self):
        return self.run('start')

    def run(self, action_name):
        ret = 0
        while True:
            act = self.ak.get_action(action_name)
            if act.act_type == 'start':
                action_name = act.to()
                continue
            elif act.act_type == 'end':
                break
            elif act.act_type == 'decision':
                action_name = act.to()
                continue
            elif act.act_type == 'fork':
                forked_actions = [self.ak.get_action(i) for i in act.node['fork_nodes']]
                act.set_fork_actions(forked_actions)
                rret = act.run()
                if rret == 0:
                    action_name = act.to()
                else:
                    print "\n\n\nAction %s run error, please check it!" % act.get_name()
                    ret = 3
                    break
            elif act.act_type in ['pig', 'ssh', 'fs', 'mr', 'email']:
                rret = act.run()
                if rret == 0:
                    action_name = act.to()
                else:
                    print "\n\n\nAction %s run error, please check it!" % act.get_name()
                    ret = 3
                    break
            else:
                pass
        return ret
