#!/usr/bin/python3
#
# dns-parse.py
# Extracts base32-encoded data exfiltrated to Bind query logs or private Burp Collaborator output
#
# Private Burp Collaborator output may be logged via 'tee' (requires "logLevel" : "DEBUG" in collaborator.config):
# java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
#
# Eric Conrad
# https://ericconrad.com
# 
# Todo list:
# - Decode base32 natively
# - Add hex decoding
# - Detect compressed data and automatically decompress

import re
import sys

if (len(sys.argv)==3):
  dnsname=sys.argv[1]
  logname=sys.argv[2]
  base32=''
  with open(logname) as f:
    for line in f:
      if dnsname in line:
        # Split the line, using all non-alphanumeric characters as delimiters. The base32-encoded
        # label (DNS name) is the 13th field in a bind query log and the 19th field in a Burp
        # Collaborator log. The 7th field can be used to distingish bind ('client') from Burp
        # Collaborator ('Received')
        substring=re.split('\W+',line) 
        if (substring[7] == 'client'): # Bind query log
          base32+=substring[13]
        elif (substring[7] == 'Received'): # Burp Collaborator log
          base32+=substring[19]
  # base32 uses '=' signs to pad to an 8-byte boundary, restore any that are missing
  pad='=' * (abs(len(base32) % -8))
  base32+=pad
  print(base32)
else:
  print('Usage: %s <DNS name> <log name>' % sys.argv[0])
