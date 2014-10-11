#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import sys

base_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath("%s/../" % base_dir))

from poze.core import *
from simple_nodes import nodes as test_nodes

ak = ActionKeeper(test_nodes)
ak.check_actions()
print ak
print ak.get_action('start')
print ak.get_action('first_pig')
print ak.get_action('end')

wfj = WorkFlowJob(ak)
#ret = wfj.start()
#print "\n\n\nWork Flow Job runs over, ret = %s." % ret
