#!/usr/bin/python
################################################################################
# @Title: lightweight_client.py
#
# @Author: Phil Smith
#
# @Date: Thu, 16-Mar-17 04:55AM
#
# @Project: Python Examples
#
# @Purpose: Create a generic TCP or UDP client that can be extended with
#           pluggable functions
#
#
################################################################################
import socket

class TestClient(object):
    """
    Generic client class
    """

    def __init__(self, ip="0.0.0.0", port=12345, proto="tcp"):
        """
        Initialize a generic client object
        """

        self.ip = ip
        self.port = port
        self.proto = proto

        if self.proto.lower() == "tcp":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.proto.lower() == "udp":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self):
        """
        Connect the client to the server and perform the action
        """

        self.socket.connect((self.ip, self.port))

if __name__ == '__main__':

    c = TestClient(proto="udp")

    c.connect()
    c.socket.send("Hello")
