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

        client = {}
        l = self.rfile.read().decode('utf-8')
        l_split = l.split()
        Expires = int(l_split[2])
        RESPUESTA = "SIP/2.0 200 OK\r\n\r\n"

        if Expires > 0:
            client["sc"] = [l_split[0]]
            client["ip"] = [self.client_address[0]]
            self.wfile.write(bytes(RESPUESTA, 'utf-8'))
            print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
            print("Expires:", " ", Expires, '\r\n\r\n' )

        elif Expires == 0:
            client = {}
            self.wfile.write(bytes(RESPUESTA, 'utf-8'))
            print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
            print("Expires:", " ", '0\r\n\r\n' )



if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', int(sys.argv[1])),SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
