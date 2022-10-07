#!/usr/bin/python3
import imaplib
import email
import calendar
import os
from email.header import decode_header
from datetime import datetime

# email account credentials
username = "archive@your_domain.com"
password = "email_password"
imap_server = "mail.your_domain.com"

#special topics for which dedicated folder will be created to store documents
special_subjects = {
        "insurance": ["insurance"],
        "medical": ["medical", "analisys", "blood test"]
        }

##Linux storage
storage_location = '{}{}{}'.format("/volume1/EmailArchiveStorage/", \
        str(datetime.now().year), \
        "/") 

#Windows storage
#storage_location = '{}{}{}'.format("C:\\Users\\Sorin\\source\\repos\\NASEmailArchiver\\", \
#                                    str(datetime.now().year), \
#                                    "\\")

def imap_connect():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    return imap

def mark_email_as_deleted(imap, i):
    # mark the mail as deleted
    imap.store(str(i), "+FLAGS", "\\Deleted")
    imap.expunge()

def close_connection_logout(imap):
    # close the connection and logout
    imap.close()
    imap.logout()

def get_special_folder(subject):
    for word in subject.lower().split():
        for topic in special_subjects:
            if word in special_subjects[topic]:
                return topic
    return ""

def get_clean_folder(root_location, subject):
    # clean text for creating a folder
    fname = "".join(c if c.isalnum() else " " for c in subject) 
    fname = fname.strip()

    #check if this is a special folder
    special_folder = get_special_folder(fname)
    if len(special_folder) > 0:
        root_location = '{}{}{}'.format(root_location, \
            special_folder, \
            os.path.sep)

    #create folder before using it further to create subfolder
    create_folder_if_not_existing(root_location)

    #concat root folder location to file name
    fname = '{}{}{}{}{}{}'.format(root_location, \
        calendar.month_abbr[datetime.now().month], " ", \
        str(datetime.now().day), " - ",\
        fname[0:128])

    create_folder_if_not_existing(fname)

    return fname

def create_folder_if_not_existing(newFolder):
    if not os.path.isdir(newFolder):
        os.mkdir(newFolder)

def download_save_email_body(body, filepath):
    open(filepath, "w", encoding="utf-8").write(body)

def download_save_attachment(part, folder_name, filename):
    filepath = os.path.join(folder_name, filename)
    
    # download attachment and save it
    open(filepath, "wb").write(part.get_payload(decode=True))

class EmailObject:
  def __init__(self, message):
    self.subject, self.encoding = decode_header(message["Subject"])[0]
    
    if isinstance(self.subject, bytes):
                    # if it's a bytes, decode to str
                    self.subject = self.subject.decode(self.encoding)
    
    # decode email sender
    self.email_from, self.encoding = decode_header(message.get("From"))[0]
    if isinstance(self.email_from, bytes):
        self.email_from = self.email_from.decode(encoding)

def main():
    create_folder_if_not_existing(storage_location)

    imap = imap_connect()

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
            
                email_object = EmailObject(msg)

                folder_name = get_clean_folder(storage_location, email_object.subject)
                

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                    
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                        if "attachment" in str(part.get("Content-Disposition")):
                            # download attachment
                            filename = part.get_filename()
                            
                            if filename:
                                download_save_attachment(part, folder_name, filename)
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()

                download_save_email_body(body, os.path.join(folder_name, "message.html"))
                mark_email_as_deleted(imap, i)

                print('{}{}'.format("processed:  ", email_object.subject))

    close_connection_logout(imap)

if __name__ == "__main__":
    main()

