#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Test_SMTP.py
#  Copyright 2020-01-19 Stephen Milheim


def main(args):
    return 0
def email():  #subject="Test", toaddrs = 'smilheim@gmail.com'):
    import smtplib
    # Here are the email package modules we'll need
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    email_address  = 'smilheim@gmail.com'
    fromaddr = 'bozemanraspberrypi@gmail.com'
    email_password='Jetson2013'
    m = MIMEMultipart()
    m['Subject'] = "Test"
    m['From'] = fromaddr
    m['To'] = email_address
    username = fromaddr
    password = email_password
    #updateFile=open(TEXT_File,'r')
    #my_message=updateFile.read()
    #updateFile.close()
    txt = MIMEText("Testing") #(my_message)
    m.attach(txt)
    # if toaddrs == email_address:
        # for box in xbeeboxobjects:
            # plotData(box)
            # try:
                # PNGfile=('{0}/{1}.png'.format('/tmp',box.name))
                # fp = open(PNGfile, 'rb')
                # img = MIMEImage(fp.read())
                # fp.close()
                # m.attach(img)
                # with open(PNGfile,'w') as fp:  # clean file
                    # pass
            # except Exception e:
                # if DEBUG:
                    # print e
                # else:
                    # pass
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, m.as_string())
    server.quit()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
    email()
