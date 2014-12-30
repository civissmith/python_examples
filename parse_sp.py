#!/usr/bin/python -B
################################################################################
# @Title: parse_sp.py
#
# @Author: Phil Smith
#
# @Date: Mon, 29-Dec-14 09:20PM
#
# @Project: Python Examples
#
# @Purpose: Parse the output of shelling out.
#
#
################################################################################
import subprocess as sp

# Motivation:
# It is often useful to have Python parse the output of a shell command.
# The subprocess.call() and subprocess.check_output() functions only 
# return the status of the command that they execute.
# 
# Consider the following command:
# $ grep -r foo *
#
# It could be useful to parse the output and perform some operation on
# the files that contain 'foo'. The call() and check_output() functions
# will not give the Python application access to those names. The
# subprocess.Popen() function can be used to get the names.

def call_sp():
  """
  This function shells out to a canned shell command. It demonstrates
  how to parse the output.
  """

  # The command can be a regular string. It does not need to be
  # a list (like call() or check_output())
  command = "grep __main__ *"

  # Popen arguments 'shell' and 'stdout' should be set otherwise
  # exceptions will be thrown
  proc = sp.Popen(command, shell=True, stdout=sp.PIPE)

  # Note that readlines() is called on the stdout member. Using
  # read() or readline() will give a list of characters.
  # Ex.
  # <line data> "Hello World!"
  # 
  # read()       - ['H','e','l','l','o',' ','W','o','r','l','d','!']
  # readline()   - ['H','e','l','l','o',' ','W','o','r','l','d','!']
  # readlines()  - 'Hello World!'
  output = proc.stdout.readline()

  for line in output:
    print line.strip()

if __name__ == "__main__":
  call_sp()
