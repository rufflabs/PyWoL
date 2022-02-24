#!/usr/bin/env python

# Notes:
# I Need mac address, ip to send to.

import sys
import socket
from binascii import unhexlify

def build_packet(mac_string):
	# mac_string will be a string of mac address
	# Remove possible :'s or -'s
	mac_hex = []
	for char in mac_string:
		if char != '-' and char != ':':
			mac_hex.append(char)
	
	mac = "".join(mac_hex)
	bytes = bytearray(102)
	
	position = 0
	while position <= 5:
		bytes[position] = b'\xff'
		position += 1
		
	while position <= 101:
		for byte in unhexlify(mac):
			bytes[position] = byte
			position += 1
	
	return bytes
	
	
wol_packet = build_packet(sys.argv[1])

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.sendto(wol_packet, (sys.argv[2], 9))
