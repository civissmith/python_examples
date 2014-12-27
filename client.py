#!/usr/bin/python -B
################################################################################
# Copyright (c) 2014 Phil Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
################################################################################
# @Title: client.py
#
# @Author: Phil Smith
#
# @Date: Thu, 25-Dec-14 06:19PM
#
# @Project: Python Examples
#
# @Purpose: Client test app.
#
################################################################################
import socket

class Client(object):
  """
  Client class for local socket test.
  """

  def __init__(self):
    """
    Initialize structures.
    """
    self.sock = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )


  def test_connect(self):
    self.sock.connect("/tmp/server_socket") 
    self.sock.send("print_cmd Once upon a midnight dreary")
    self.sock.send("print_cmd while I pondered weak and weary")
    self.sock.send("print_cmd over many a quaint and curious volume of forgotten lore")
    self.sock.send("print_cmd while I pondered, nearly napping")
    self.sock.send("print_cmd suddenly there came a tapping")
    self.sock.send("print_cmd as of someone gently rapping, rapping at my chamber door")
    self.sock.send("quit_cmd")


if __name__ == "__main__":
  cli = Client()
  cli.test_connect()
