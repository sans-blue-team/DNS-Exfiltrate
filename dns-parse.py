#!/usr/bin/python3
#
# dns-parse.py
# Extracts base32-encoded data exfiltrated to Bind query logs or private Burp Collaborator output
#
# Private Burp Collaborator output may be logged via 'tee':
# java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
#
# Eric Conrad
# https://ericconrad.com
import re
import sys

if ((len(sys.argv)==4) and ((sys.argv[3]=='bind') or (sys.argv[3]=='collaborator'))):
  dnsname=sys.argv[1]
  logname=sys.argv[2]
  logtype=sys.argv[3]
  base32=''
  with open(logname) as f:
    for line in f:
      if dnsname in line:
        # Split the line, using all non-alphanumeric characters as delimiters. The hostname (first 
        # label) is the 19th field in a Burp Collaborator log and the 13th field in a bind query log
        substring=re.split('\W+',line) 
        if logtype == 'collaborator':
          base32+=substring[19]
        elif logtype == 'bind':
          base32+=substring[13]
  # base32 uses '=' signs to pad to an 8-byte boundary, restore any that are missing
  pad='=' * (8-(len(base32) % 8))
  base32+=pad
  print(base32)
else:
  print('Usage: %s <DNS name> <log name> (bind|collaborator)' % sys.argv[0])
