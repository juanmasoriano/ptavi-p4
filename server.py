#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):

        self.registered = {}
        l = self.rfile.read().decode('utf-8')
        l_split = l.split()
        Expires = int(l_split[2])
        RESPUESTA = "SIP/2.0 200 OK\r\n\r\n"

        Fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        Seg = int(Fecha[17:])

        Fecha1 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Expires))
        Seg1 = Expires

        SegTot = Seg + Seg1

        Tiempo = Fecha, "+" + Fecha1[11:]

        if Expires > 0:
            self.registered["sc"] = [l_split[0]]
            self.registered["address"] = [self.client_address[0]]
            self.registered["expires"] = [Tiempo]
            self.wfile.write(bytes(RESPUESTA, 'utf-8'))
            print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
            print("Expires:", " ", Expires, '\r\n\r\n' )
            self.register2json()
        elif Expires == 0:
            self.registered = {}
            self.wfile.write(bytes(RESPUESTA, 'utf-8'))
            print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
            print("Expires:", " ", '0\r\n\r\n' )
            self.register2json()

    def register2json(self):

        with open('registered.json', 'w') as file:
            json.dump(self.registered,file)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', int(sys.argv[1])),SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
