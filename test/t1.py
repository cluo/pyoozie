#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import sys

base_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath("%s/../" % base_dir))

from poze.core import *

act = {
    'name': 'a1',
    'to': 'a2',
}


action = Action(act)
print action

print ""
start_action = StartAction(act)
print start_action

print ""
end_action = EndAction(act)
print end_action
