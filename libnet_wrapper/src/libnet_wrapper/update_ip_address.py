#!/bin/python3
# https://github.com/vc12345679/NI_GPIB_ENET_Py3 Reference this heavily
import socket
from struct import pack


packet = b'\x00802f10d115d05099c187ed80350001080006040004d05099c187ed0A02000800802f10d1150A020009'
print(packet)

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
s.bind(("enp7s0",0))
s.send(packet)
