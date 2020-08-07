#!/usr/bin/python

import imaplib
import re
import yaml
import os

M=imaplib.IMAP4_SSL('imap.gmail.com')

cwd: str = os.path.abspath(os.path.dirname(__file__))
dirs: list = cwd.split('/')
cwd = ''
for x in range(5):
	cwd += dirs[x]
	cwd += '/'
os.chdir(cwd)
if not os.path.exists("credenciales.yml"):
	ar = open(cwd + "credenciales.yml", "x+")
	ar.write("""email:
password:
""")
	ar.close()


with open(cwd + "credenciales.yml") as f:
	credenciales = yaml.load(f, Loader=yaml.FullLoader)
	M.login(credenciales['email'], credenciales['password'])

	status, counts = M.status("INBOX","(MESSAGES UNSEEN)")

	if status == "OK":
		unread = re.search(r'UNSEEN\s(\d+)', counts[0].decode('utf-8')).group(1)
	else:
		unread = "N/A"

	print(unread)
