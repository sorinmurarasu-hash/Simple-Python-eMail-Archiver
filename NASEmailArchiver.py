#!/usr/bin/python3
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os


def clean_and_format(text):
    # clean text for creating a folder
    fname = "".join(c if c.isalnum() else " " for c in text) 
    fname = fname.strip()
    return fname[0:128]

# account credentials
username = "arhiva@myDomain"
password = "MySecretPassword"
imap_server = "DomainImapServer"

##NAS Linux storage
storage_location = "/Volume1/MailArchive/" + str(datetime.now().year) + "/"

#Windows storage
#storage_location = "C:\\Users\\gv10qc\\source\\repos\\NASEmailArchiver\\NASEmailArchiver\Arhiva\\"
#storage_location = ""
#storage_location += str(datetime.now().year) + "\\"

if not os.path.isdir(storage_location):
    os.mkdir(storage_location)

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)

status, messages = imap.select("INBOX")
#get number of emails
messages = int(messages[0])

for i in range(messages, 0, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")

    for response in msg:
        if isinstance(response, tuple):
            # create a message object
            msg = email.message_from_bytes(response[1])
            # get the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)

            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

                    if "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = storage_location + clean_and_format(subject)
                            if not os.path.isdir(folder_name):
                                os.mkdir(folder_name)
                            
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                body = msg.get_payload(decode=True).decode()

            folder_name = storage_location + clean_and_format(subject)
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            
            filename = "message.html"
            filepath = os.path.join(folder_name, filename)

            open(filepath, "w", encoding="utf-8").write(body)

            # mark the mail as deleted
            imap.store(str(i), "+FLAGS", "\\Deleted")
            imap.expunge()

# close the connection and logout
imap.close()
imap.logout()


