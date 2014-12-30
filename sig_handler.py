#!/usr/bin/python -B
################################################################################
# @Title: sig_handler.py
#
# @Author: Phil Smith
#
# @Date: Mon, 29-Dec-14 08:36PM
#
# @Project: Python Examples
#
# @Purpose: Example demonstrating how to create signal handlers.
#
#
################################################################################
import signal

def main():
  """
  This function attaches a signal handler for SIGINT. It creates an infinite
  loop so the user must manually kill the process.
  """
  
  # Attach the signal handler
  # Signal will catch ctrl+c
  signal.signal( signal.SIGINT, sigint_handler )

  while True:
    pass

def sigint_handler( number, stack_frame ):
  """
  This is the function that will respond to the SIGINT signal.
  """
  print "\nSIGINT received!"
  print "Number:"
  print number
  print "Stack Frame:"
  print stack_frame.f_code
  exit(0)


if __name__ == "__main__":
   main()
