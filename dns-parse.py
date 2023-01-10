#!/usr/bin/python3
#
# dns-parse.py
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
        substring=re.split('\W+',line) 
        if logtype == 'collaborator':
          base32+=substring[19]
        elif logtype == 'bind':
          base32+=substring[13]
  pad='=' * (8-(len(base32) % 8))
  base32+=pad
  print(base32)
else:
  print('Usage: %s <DNS name> <log name> (bind|collaborator)' % sys.argv[0])
