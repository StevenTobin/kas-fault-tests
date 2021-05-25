#!/usr/bin/env python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from subprocess import run
from subprocess import PIPE
from scripts.logger import log

def get_cmd_output(cmd:str) -> (str):  
  log.debug('[CMD] ' + cmd.rstrip("\n"))
  cmd = cmd.split(" ")
  output = run(cmd, stdout=PIPE).stdout.decode("utf-8").rstrip("\n")
  log.debug('[CMD] ' + output)
  return output
