#!/usr/bin/env python

import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to any IP, port 9
udp_socket.bind(('', 9))

print('PyWoL: Wake-On-LAN Listener\n==============================')
print('Listening for WoL packets on port 9.\n\n')

while True:
    data, _ = udp_socket.recvfrom(1024)

    # Setup variable to hold our string.
    payload = []
    
    for char in data:
        raw_bit = hex(ord(char))
        bit = raw_bit[2:]
        if bit == '0':
            bit = '00'
        payload.append(bit)
        
    # Check if packet is actually a WoL packet, and starts with 6 0xFF
    if payload[:6] == ['ff', 'ff', 'ff', 'ff', 'ff', 'ff']:
        valid_wol = True
    else:
        valid_wol = False

    if valid_wol:
        # Remove 6 0xFF's
        del payload[:6]
        
        # Compare two iterations of the MAC to make sure it's valid.
        mac_address = payload[:6]
        second_mac = payload[6:12]
        
        if mac_address == second_mac:
            mac_address = payload[:6]
            print('WoL for MAC: ' + ":".join(mac_address))
