#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys
try:
# Constantes. Dirección IP del servidor y contenido a enviar
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METODO = sys.argv[3]
    DIR = sys.argv[4]
    TIEMPO = sys.argv[5]
    line = DIR + " " + METODO + " " + TIEMPO
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:

        my_socket.connect((SERVER, PORT))
        print("Enviando:", line, "seg",'\r\n\r\n')
        my_socket.send(bytes(line, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
    print("Socket terminado.")

except IndexError:
    print("Usage: client.py ip puerto register sip_address expires_value")
