#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
 

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        RESPUESTA = "SIP/2.0 200 OK\r\n\r\n"
        client = {}
        self.wfile.write(bytes(RESPUESTA, 'utf-8'))

        l = self.rfile.read().decode('utf-8')
        l_split = l.split()
        client["sc"] = [l_split[0]]
        client["ip"] = [self.client_address[0]]


        print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n\r\n')



if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', int(sys.argv[1])),SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
