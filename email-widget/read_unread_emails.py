#!/usr/bin/python

import imaplib
import email
import datetime
import yaml
import os

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


def process_mailbox(mailbox):
    rv, data = mailbox.search(None, "(UNSEEN)")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = mailbox.fetch(num, '(BODY.PEEK[])')
        if rv != 'OK':
            print("ERROR getting message", num)
            return
        msg = email.message_from_bytes(data[0][1])
        for header in ['From', 'Subject', 'Date']:
            hdr = email.header.make_header(email.header.decode_header(msg[header]))
            if header == 'Date':
                date_tuple = email.utils.parsedate_tz(str(hdr))
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    print("{}: {}".format(header, local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            else:
                print('{}: {}'.format(header, hdr))
        # with code below you can process text of email
        # if msg.is_multipart():
        #     for payload in msg.get_payload():
        #         if payload.get_content_maintype() == 'text':
        #             print  payload.get_payload()
        #         else:
        #             print msg.get_payload()


f = open(cwd + "credenciales.yml")
credenciales = yaml.load(f, Loader=yaml.FullLoader)
M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login(credenciales['email'], credenciales['password'])
M.select("INBOX")
rva, data1 = M.select("INBOX")
if rva == 'OK':
    process_mailbox(M)
M.close()
M.logout()
