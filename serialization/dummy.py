#!/usr/bin/python -B
################################################################################
# @Title: dummy.py
#
# @Author: Phil Smith
#
# @Date: Fri, 02-Jan-15 10:18AM
#
# @Project: Python Examples
#
# @Purpose: A dummy class to be used as ADT surrogate.
#
#
################################################################################

class Dummy(object):
  """ 
  This is a dummy class. It can be used as stand-in for more complex user-defined
  types.
  """

  def __init__( self, field1=None ):
    self.field1 = field1

  def test(self):
    print "The value of field1 is %s" % self.field1
