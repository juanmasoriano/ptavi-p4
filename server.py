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
    
    registered = {}
    RESPUESTA = "SIP/2.0 200 OK\r\n\r\n"
    def handle(self):


        l = self.rfile.read().decode('utf-8')
        l_split = l.split()
        Expires = int(l_split[2])


        Fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

        Fecha1 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Expires))

        Tiempo = Fecha, "+" + Fecha1[11:]
        Expiracion = time.time() + Expires

        if Expiracion > time.time():
            try:
                self.json2registered()
                if self.registered != {}:
                    print("REGISTER", " ",'sip:',self.registered['sc']," ",'SIP/2.0\r\n')
                    print("Expires:", " ", self.registered['expires'],'\r\n\r\n' )
                    print(self.registered)
                elif self.registered == {}:
                    raise FileNotFoundError
                else:
                    raise FileNotFoundError

            except FileNotFoundError:

                if Expires > 0:
                    self.registered["sc"] = [l_split[0]]
                    self.registered["address"] = [self.client_address[0]]
                    self.registered["expires"] = [Tiempo]
                    self.register2json()

                    self.wfile.write(bytes(self.RESPUESTA, 'utf-8'))
                    print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
                    print("Expires:", " ", Expires, '\r\n\r\n')
                    print(self.registered)


                elif Expires == 0:
                    self.registered = {}
                    self.register2json()

                    self.wfile.write(bytes(self.RESPUESTA, 'utf-8'))
                    print("REGISTER", " ",'sip:',l_split[0]," ",'SIP/2.0\r\n')
                    print("Expires:", " ", '0\r\n\r\n' )
                    print(self.registered)
        else:

            self.registered = {}
            self.register2json()
            print(self.registered)

    def register2json(self):

        with open('registered.json', 'w') as file:
            json.dump(self.registered,file)

    def json2registered(self):

        with open('registered.json', 'r') as file:
            self.registered = json.load(file)
        self.wfile.write(bytes(self.RESPUESTA, 'utf-8'))


if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request

    serv = socketserver.UDPServer(('', int(sys.argv[1])),SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
