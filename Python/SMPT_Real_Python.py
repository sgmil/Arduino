#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SMPT_Real_Python.py
#  Copyright 2020-01-19 Stephen Milheim

import smtplib, ssl
def main():

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "bozemanraspberrypi@gmail.com"
    receiver_email = "smilheim@gmail.com"
    password = "Jetson2013"
    message = """\
    Temperature Monitors

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:

        server.starttls(context=context)

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    return 0

if __name__ == '__main__':
    main()
