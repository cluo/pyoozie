#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import os
import sys

base_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath("%s/../" % base_dir))

from poze.core import *
from decision_nodes import nodes as fnodes

ak = ActionKeeper(fnodes)
ak.check_actions()
wfj = WorkFlowJob(ak)
ret = wfj.start()
print "\n\n\nWork Flow Job runs over, ret = %s." % ret
