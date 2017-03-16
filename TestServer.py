#!/usr/bin/python
################################################################################
# @Title: TestServer.py
#
# @Author: Phil Smith
#
# @Date: Thu, 16-Mar-17 04:55AM
#
# @Project: Python Examples
#
# @Purpose: Provide a class to generate generic TCP or UDP servers with a
#           defined callback.
#
################################################################################
import socket
import threading

class TestServer(object):
    """
    Lightweight network server.
    """

    def __init__(self, ip='0.0.0.0', port=12345, proto='tcp', backlog=2,
                 action=None):
        """
        Create the server object and set default service IP:Port and the
        protocol.
        """

        self.ip = ip
        self.port = port
        self.proto = proto
        self.backlog = backlog
        if action == None:
            self.action = self.close_immediate
        else:
            self.action = action

        # Protocol determines bind/socket parameters
        if proto.lower() == "tcp":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            # The given protocol is not understood
            raise RuntimeError("{} is not a supported protocol".format(self.proto))

    def close_immediate(self, client=None, address=None):
        """
        Close the connection and do nothing else
        """
        if client is not None:
            client.close()

    def serve(self):
        """
        Run the server
        """

        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.backlog)

        print (" - Listening on {}:{}".format(self.ip, self.port))

        while True:

            client, address = self.socket.accept()

            connection_thread = threading.Thread(target=self.action, args=(client, address))
            connection_thread.start()


if __name__ == '__main__':
    def report_connection(client=None, address=None):
        """
        Print a message showing that connection was made.
        """

        print ("Connection made from {}:{}".format(address[0],address[1]))
        client.close()

    s = TestServer(port=12346)
    s.action = report_connection
    s.serve()
