#!/usr/bin/python3
#
# dns-parse.py v0.3
# Extracts and converts hex- or base32-encoded data exfiltrated to Bind query logs or private Burp Collaborator output
#
# Private Burp Collaborator output may be logged via 'tee':
# java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
#
# Eric Conrad
# https://ericconrad.com
# 
# Todo list:
# - Detect compressed data and automatically decompress

import re
import sys
import base64

if (len(sys.argv)==3):
  dnsname=sys.argv[1]
  logname=sys.argv[2]
  chunk=''       # One chunk of hex or base32-encoded content
  base32=''      # final base32-encoded data
  hexadecimal='' # final hex-encoded data
  with open(logname) as f:
    for line in f:
      if dnsname in line:
        # Split the line, using all non-alphanumeric characters as delimiters. The hex- or
        # base32-encoded label (DNS name) is the 13th field in a bind query log and the 19th 
        # field in a Burp Collaborator log. The 7th field can be used to distingish bind 
        # ('client') from Burp Collaborator ('Received')
        substring=re.split('\W+',line) 
        if (substring[7] == 'client'): # Bind query log
          chunk+=substring[13]
        elif (substring[7] == 'Received'): # Burp Collaborator log
          chunk+=substring[19]
  if re.search("^[A-Z2-7]*$",chunk): # base32
    base32=chunk
    # base32 uses '=' signs to pad to an 8-byte boundary, restore any that are missing
    pad='=' * (abs(len(base32) % -8))
    base32+=pad
    print(base64.b32decode(base32).decode(),end='')
  elif re.search("^[0-9a-f]*$",chunk): # Hex
    hexadecimal=chunk
    print(bytes.fromhex(hexadecimal).decode('utf-8'),end='')
  else:
    print('Error: data does not appear to be hex- ([9-0a-fa]) or base32-encoded (A-Z2-7])')
else:
  print('Usage: %s <DNS name> <log name>' % sys.argv[0])
