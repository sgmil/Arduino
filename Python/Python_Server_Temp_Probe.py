#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright 2020-01-19 Stephen Milheim
# Python Server for Temp Probes #
from flask import Flask, request
import json
import time
import datetime
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

UPDATE_TIME=8   # 8am message

app = Flask(__name__)

DEBUG=False
class Probe():
    def __init__(self, place, name, tmax, tmin):
        self.place=place
        self.name=name
        self.tmax=tmax
        self.tmin=tmin
        self.current=0
        self.updateDay=0

    def tooHot(self):
        if DEBUG:   print("%s %s is:" %(self.place,self.name))
        if (self.current>self.tmax):
            if DEBUG:   print("Too Hot.")
            #email("%s %s is too hot!" %(self.place,self.name))
        else:
            if DEBUG:   print("Not too hot")


    def tooCold(self):
        if DEBUG:   print("%s %s is:" %(self.place,self.name))
        if (self.current<self.tmin):
            if DEBUG:   print("Too Cold")
            #email("%s %s is too cold!" %(self.place,self.name),'smilheim@gmail.com')
        else:
            if DEBUG:   print("Not too cold.")

def updateTemp(pldict, pljson):
    print("updating...")
    for i in pldict.keys():
        if DEBUG:   print(i)
        if DEBUG:   print(pljson[[*pljson.keys()][0]][i])
        pldict[i].current=pljson[[*pljson.keys()][0]][i]
        pldict[i].tooHot()
        pldict[i].tooCold()
        print("Temp checked")
    if int(time.strftime('%d'))!=pldict[[*pldict.keys()][0]].updateDay and int(time.strftime('%H')) >= UPDATE_TIME:
        print("did you get email?")
        pldict[[*pldict.keys()][0]].updateDay=int(time.strftime('%d'))
        email('Today\'s Update')


Garage={"fridge":Probe("Garage", "fridge", 39,33),\
        'freezer':Probe("Garage","freezer",24,0),\
        'ambient':Probe("Garage","ambient",100,0)}

#e={"Garage":{"freezer":-2,"fridge":42,"ambient":67}}



@app.route("/")
def home():
    nam = "Steve"
    print ("Requested")
    return "Hello,%s" %(nam)

@app.route('/json-post', methods = ['POST'])
def postjsonHandler():
    if DEBUG:   print (request.is_json)
    content = request.get_json()
    print (content)
    if DEBUG:   print(type(content))
    if DEBUG:   print([*content.keys()][0])
    if DEBUG:   print(type([*content.keys()][0]))
    if (([*content.keys()][0])=="Garage"):
        updateTemp(Garage,content)
    return 'JSON posted'

def email(subject="Test"):
    port = 587  # For starttls
    toaddrs  = 'smilheim@gmail.com'
    fromaddr = 'bozemanraspberrypi@gmail.com'
    email_password='Jetson2013'
    m = MIMEMultipart()
    m['Subject'] = subject
    m['From'] = fromaddr
    m['To'] = toaddrs
    username = fromaddr
    password = email_password
    context = ssl.create_default_context()
    #updateFile=open(TEXT_File,'r')
    #my_message=updateFile.read()
    #updateFile.close()
    my_message="Garage \n"
    for i in Garage.keys():
        my_message=my_message+Garage[i].name+"\t\t"+str(Garage[i].current)+"\n"
    txt = MIMEText(my_message) #(my_message)
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
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls(context=context)
    #server.ehlo()
   #server.starttls()
    #server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, m.as_string())
    server.quit()
    return 0


if __name__ == "__main__":
    #email()
    #print ("did email send?")
    app.run(host='192.168.0.106',port=5050, debug=True)
