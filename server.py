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
# @Title: server.py
#
# @Author: Phil Smith
#
# @Date: Thu, 25-Dec-14 06:19PM
#
# @Project: Python Examples
#
# @Purpose: Server test app.
#
################################################################################
import os
import sys
import atexit
import socket
import signal
import os.path as op

class Server(object):
  """
  The server class to practice BSD sockets.
  """


  def __init__(self):
    # Init a command queue
    self.cmd_q = []

    # Init the event dict
    self.event_funcs = {}

    self.rx_socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
    self.rx_endpoint = "/tmp/server_socket"
    self.tx_endpoint = "/tmp/client_socket"


  def enqueue_cmd(self, cmd):
    """
    Add a command to the server command queue.
    """
    self.cmd_q.append(cmd)


  def dequeue_cmd(self):
    """
    Dequeues the command at the head of the queue.
    """

    # Don't attempt to process an empty queue.
    if not self.cmd_q:
      return None

    # Return the head element.
    return self.cmd_q.pop(0)


  def register_event(self, name, func):
    """
    Registers event handler functions. 
    """
    self.event_funcs[name] = func


  def quit_event(self):
    """
    Event handler to handle the "quit" command.
    """

    print "Shutting down."
    self.rx_socket.close()
    os.remove( self.rx_endpoint )
    exit(0)


  def print_event(self, args=None):
    """
    Test event handler for multi-argument commands.
    """
    print args


  def connect_rx(self):
    """
    Connects this app to it's rx socket.
    """

    # Socket already in use will return socket.error(98)
    # Get rid of it before trying to connect.
    # Note: must check for 'exists' no 'isfile' because sockets
    #       are not "files".
    if op.exists( self.rx_endpoint ):
      os.remove( self.rx_endpoint )

    # Set the socket to non-blocking
    self.rx_socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
    self.rx_socket.setblocking(0)

    try:
      self.rx_socket.bind( self.rx_endpoint )
    except Exception as e:
      print e.args
      print "Could not connect to socket: %s" % self.rx_endpoint
      exit(1)


  def listen(self):
    """
    Listen to the socket for incoming data.
    """

    # Check for new data
    # If new data is available:
    #   Enqueue the command and proceed

    # Since the socket is non-blocking, handle the 
    # "Resource temporarily unavailable" exception.
    try:
      raw_data = self.rx_socket.recv(4096)

    except socket.error as err:
      if err.args[0] == 11:
        return
      # If the exception was not the "Resource temporarily unavailable"
      # then something bad happened and should be reported.
      print "Fatal Exception: ",
      print err.args[1]
      exit(1)

    # To get here, data must have been recieved. Pre-check it and
    # enqueue if necessary.
    # <takes> "CMD_NAME ARG1 ARG2"
    # <becomes> ['cmd_name', 'arg1', 'arg2']
    # So, data[0] = command
    # And data[1:] = args
    # So enqueue needs to add commands and args:
    # (cmd, args[])
    data = raw_data.lower().split() 
    cmd = data[0]
    # If command is no-argument, then args will be the empty list.
    args = data[1:]

    if cmd in self.event_funcs:
      self.enqueue_cmd( (cmd, args) )


  def process_cmds(self):
    """
    Process the commands in the command queue.
    """
    element = self.dequeue_cmd()
    if not element:
      return
    cmd = element[0]
    args = element[1][:]

    if cmd in self.event_funcs and args:
      for arg in args:
        self.event_funcs[cmd]( arg )
    elif cmd in self.event_funcs:
      self.event_funcs[cmd]()


  def run(self):
    """
    Main executive for the server.
    """
    if len(sys.argv) != 2:
      print('Usage: %s [start|stop]' % sys.argv[0])
      exit(1)
  
    if sys.argv[1] == 'start':
      try:
        self.daemonize('/tmp/daemon.pid')
      except Exception as err:
        print "Fatal Exception: "
        print err.args
        exit(1)

      self.register_event("quit_cmd", self.quit_event)
      self.register_event("print_cmd", self.print_event)
      self.register_event("req_cmd", self.send_data)
      self.connect_rx()
    elif sys.argv[1] == 'stop':
      if os.path.exists('/tmp/daemon.pid'):
        pidFile = open('/tmp/daemon.pid', 'r')
        pid = pidFile.read()
        print('Killing: %s' % pid)
        os.kill(int(pid), signal.SIGTERM)
      else:
        print('Daemon not running!')
        exit(1)
    else:
        print('Unknown Command!')
        exit(1)
  
    while True:
      self.listen() 
      self.process_cmds()


  def daemonize( self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    #
    # Check to see if the daemon is already running.
    #
    if os.path.exists(pidfile):
      print 'Daemon is already running'
      exit(1)
  
    #
    # This fork will detach the daemon from the parent task. (First Fork)
    #
    try:
      if os.fork() > 0:
        exit(0) 
  
    except OSError:
      print 'First fork has failed! Quitting...'
      exit(2)
  
    #
    # Change the cwd so that the daemon gives up any links to it.
    #
    os.chdir('/')
    os.umask(0)
    os.setsid()
  
    #
    # This fork will cause the daemon to relinquish session leadership. (Second Fork)
    #
    try:
      if os.fork() > 0:
        exit(0)
    except OSError:
      print('Second fork has failed! Quitting...')
      exit(2)
  
    #
    # Flush all of the I/O buffers.
    #
    sys.stdout.flush()
    sys.stderr.flush()
  
    #
    # The file descriptors for stdin/out/err should be replaced.
    #
    os.dup2(0, 2)
    os.dup2(0, 3)
  
    #
    # Write the PID into the PID file.
    #
    pf = open(pidfile, 'w')
    pid = os.getpid()
    print pid
    pf.write(str(pid))
    pf.close()
  
    #
    # Delete the PID file when the daemon exits
    #
    atexit.register(lambda: os.remove(pidfile))
  
    #
    # Create a signal handler to kill the daemon
    #
    def sigterm_handler(signo, frame):
      print("Caught SIGTERM!")
      exit(0)
  
    signal.signal(signal.SIGTERM, sigterm_handler)


  def send_data(self):
    self.tx_socket = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
    self.tx_socket.connect( self.tx_endpoint )
    self.tx_socket.send("Hello World")


if __name__ == "__main__":

  # Test the server app.
  serv = Server()
  serv.run()
