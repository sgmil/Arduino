#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  SensorBoxClass.py
#  
#  Copyright 2016 Stephen Milheim <sgmil@quadcore>
#  
''' 
This program runs on a server with an xbee coordinator attached to usb port.  
The remote sensors send intermittent data through remote xbees to coordinator
using API 2 mode. 
Temperature sensors and posttel work.  Gardentel is in progress.  
Setup data imported from '/home/sgmil/Dropbox/PROJECTS/SensorNetwork/SteveSensorNetwork/datainput.csv'

This is a transition of original xbeeSensor program to incorporate better use of classes
with  the SensorBoxClass with Temp and Battery etc subclasses.  
Reading in data from csv file to allow for easier changes.  
Need to implement better error control to prevent program crashes.  
FIXES:
7 Feb: store data in /tmp- won't be accessible in Dropbox but can access through xively or google.site
'''
# 
import ast
import csv
from xbee import XBee, ZigBee
import serial
import time
import pprint
import xively_upload_steve as xively 
    # sudo pip install xively-python --pre
from numpy import loadtxt
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#import os
import subprocess
from prettytable import PrettyTable
import multiprocessing
import datetime

##
PORT="/dev/xbeesensors" 
BAUD_RATE = 9600
NOMAX=120
NOMIN=-30
#FREEZER_TEMP_THRESHOLD=25
#INSIDE_TEMP_THRESHOLD=40
#fridge_TEMP_THRESHOLD=51
BATTERY_THRESHOLD=2.6
AM_ALERT_TIME = 8 # first morning alert
PM_ALERT_TIME  = 22 # last evening alert
ALERT_FREQUENCY = 2 # interval hours between alerts
UPDATE_TIME = 8
SENSOR_TIME = 20 # amount of time in seconds to collect data list before averaging
#today=99
source='None'
email_address  = 'smilheim@gmail.com'
text_address  = '4062531562@vtext.com'
fromaddr = 'bozemanraspberrypi@gmail.com'
email_password='Jetson2013'
PNG_File='/tmp/Temperature.png'
TEXT_File='/tmp/message.txt'
FEED_ID = '422525771'
API_KEY = 'KDpNF9lRs1pdgP3o7idcS3ypASiBlchql2EyCmO6EyDHcrW4'
PROGRAM_DIRECTORY='/home/sgmil/Dropbox/PROJECTS/SensorNetwork/SteveSensorNetwork'
INPUT_FILE=PROGRAM_DIRECTORY+'/datainput.csv'
FETCH_REQUEST_FILE=PROGRAM_DIRECTORY+'/fetch_request.txt'
COLORS=['r','y','b', 'g','c','m','k','r']
xbeeboxobjects=[]   # the list of all box objects
tempsensorobjects=[]    #part of a box object listed here for code completion
####
DEBUG=True
TESTING=False # no Xbee
####
def capture_data(sensor): # listen for data for SENSOR_TIME seconds, add datum to list, average list, log data
    sensor.now=datetime.datetime.utcnow()
    time_dif=sensor.now-sensor.start
    if DEBUG:
        print ('New data point')
    if time_dif.total_seconds() > SENSOR_TIME:      
        if sensor.datalist:
            #if DEBUG:
                #print (sensor.datalist+ ' to average')
            average_data(sensor) # do something to average values in list and commit data
        sensor.start=sensor.now
        sensor.datalist=[sensor.current]    
    
    else:
        sensor.datalist.append(sensor.current)
        #if DEBUG:
            #print sensor.datalist
def average_data(sensor):
    sensor.current=sum(sensor.datalist)/float(len(sensor.datalist)) # get average
    sensor.current=int(round(sensor.current)) # round off to integer
    if DEBUG:
        print ("averaging {0} data points for {1}".format(len(sensor.datalist), sensor.name))
    sensor.minmaxCheck()
    sensor.alertCheck() 
    logData(sensor.box,sensor)
    #callXively(sensor.box,sensor)  
    
def check_data_time(sensor):
    # has more than SENSOR_TIME sec elapsed since last commit? Then commit data if there is some
    time_dif=datetime.datetime.utcnow()-sensor.start 
    #if DEBUG:
        #print 'checking data'
    if time_dif.total_seconds() > SENSOR_TIME:      
        if sensor.datalist: # is there data
            average_data(sensor) # commit data
            sensor.datalist=[] # clear list
                                        
def check_response(response):
    # could consider route to correct parser based on 'options' 
    try:
        if response['id'] in ['rx_io_data_long_addr', 'rx']:
            parse_response(response)
        #else: 
            #if DEBUG:
                #print ("Bad response['id'] {0}".format (response['id']))
    except Exception as e:
        if DEBUG:
            print e.message
                
def parse_response(response):
    for box in xbeeboxobjects:
        #try:
        if box.xbeeID==response['source_addr_long']:
            if DEBUG:
                print ('got response %s' % box)             
            reading='adc-'
            try:
                for (i,sensor) in enumerate(box.tempsensorobjects):
                    if DEBUG:
                        print sensor
                        print (int(response['samples'][0][reading+str(i)]*0.211)-58)+ sensor.correction 
                    sensor.current=((int(response['samples'][0][reading+str(i)])*0.211)-58) + sensor.correction
                    sensor.time=int(time.strftime('%H'))+int(time.strftime('%M'))/60.0+int(time.strftime('%S'))/3600.0
                    capture_data(sensor)
            except Exception as e:
                if DEBUG:
                    print e.message
            try:
                box.current=(response['samples'][0]['adc-7']*0.117)/100.0
                box.batteryCheck()
                if DEBUG:
                    print box.current
            except Exception as e:
                if DEBUG:
                    print e.message
            if box.posttel:
                posttel_response(box, response)
            return 0

        else:
            pass
        #except Exception as e:
        #   if DEBUG:
        #       print e.message
        
def logData(xbeeObject, sensorObject): # expect temp sensor sensorObject    
    Datafile='%s/%s.%s.dat' % ('/tmp',xbeeObject.name, sensorObject.name)
    with open(Datafile,'a') as temp:
        #temp.write(str(sensorObject.time) + " " + str(sensorObject.current) + "\n") 
        temp.write('{0:4.2f}    {1:3}\n'.format(sensorObject.time, round(sensorObject.current)))
    if DEBUG:
            print
            print ('Current temp showing on %s thermometer is %d at %s.' 
                    % (sensorObject.name, sensorObject.current, time.strftime('%H:%M')))
            print ('Min temp is %d.           Max temp is %d.' 
                    % (sensorObject.minTemp, sensorObject.maxTemp))
            print 
def callXively(xbeeObject, sensorObject):
    streamName=xbeeObject.name+"_"+sensorObject.name
    # call as new process to avoid blocking program if problem with Xively
    x=multiprocessing.Process(target=xively.DataStreamUpdate, args=(FEED_ID, API_KEY,streamName, sensorObject.current))
    x.start()
    time.sleep(10)
    x.terminate()    # if not successful in 10 seconds then terminate
    x.join()      
    return 0

def posttel_response(box, response):
    box.posttel.current = int(response['samples'][0]['dio-11']) # mail status
    box.posttel.warning=box.posttel.current
    alertMessage(box.posttel)
    box.current=(response['samples'][0]['adc-7']*0.117)/100.0 # battery status
    box.batteryCheck()   
#   callXively(box,box.posttel)

    
def clearDataFiles():
    for box in xbeeboxobjects:
        for sensor in box.tempsensorobjects:
            Datafile='%s/%s.%s.dat' % ('/tmp',box.name, sensor.name)
            with open(Datafile, 'w') as temp:
                pass
    return 0 
def fileRead(DATAFILE):  # returns x, y array, lists
    x,y = loadtxt(DATAFILE, unpack= True)
    return (x,y)    
def plotData(box): # plot from file; return 0 
    #pass
    if box.tempsensorobjects:
        for i,sensor in enumerate(box.tempsensorobjects):
            try:
                Datafile='%s/%s.%s.dat' % ('/tmp',box.name, sensor.name)
                x,y = loadtxt(Datafile, unpack= True)
                plotLabel=sensor.name
                plotColor=COLORS[i]
                plt.plot(x,y, marker='o',linestyle='',color=plotColor, label=plotLabel)
            except Exception, e:
                if DEBUG:
                    print e
                else:
                    pass
        plt.xlabel('Time of Day')
        plt.ylabel('Temperature (Fahrenheit)')
        plotTitle=('{0} Temperature Sensors'.format(box.name))
        plt.title(plotTitle, color='g')
        plt.legend(loc='lower center')
        PNGfile=('{0}/{1}.png'.format('/tmp',box.name))
        plt.savefig(PNGfile)
        plt.close()
    return 0
    
def alertMessage(self):
    with open(TEXT_File,'w') as messageFile:
        if (self.warning == 'hot') or (self.warning == 'cold'):
            location=("{0}_{1}".format(self.box.name,self.name))
            messageFile.write('Stephen, \nYour {0} is too {1}! \n'.format(location,self.warning))
            messageFile.write('The temperature on {0} at {1} is {2} degrees F.\n'.format(time.strftime('%A'), time.strftime('%H:%M'), self.current))
        elif self.warning == 'low':
            location=("{0}_{1}".format(self.box.name,self.name))
            messageFile.write('Stephen, \nYour %s battery is too %s! \nThe voltage on %s at %s is %d volts.\n' % (location, self.warning, time.strftime('%A'), time.strftime('%H:%M'), self.current))
        elif (self.warning == 1):
            messageFile.write('US post has delivered the mail!')
        elif (self.warning == 0):
            messageFile.write('Mail has been retrieved!')
        else:
            return 0
    email('', text_address)
    self.alertTime=int(time.strftime('%H'))
    if DEBUG:
        print '%s alert message sent' % self.warning
 
def email(subject, toaddrs):
    import smtplib
    # Here are the email package modules we'll need
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart  
    from email.mime.text import MIMEText
    m = MIMEMultipart()
    m['Subject'] = subject
    m['From'] = fromaddr
    m['To'] = toaddrs
    username = fromaddr
    password = email_password   
    updateFile=open(TEXT_File,'r')
    my_message=updateFile.read()
    updateFile.close()
    txt = MIMEText(my_message)
    m.attach(txt)
    if toaddrs == email_address:
        for box in xbeeboxobjects:
            plotData(box)
            try:
                PNGfile=('{0}/{1}.png'.format('/tmp',box.name))
                fp = open(PNGfile, 'rb')
                img = MIMEImage(fp.read())
                fp.close()
                m.attach(img)
                with open(PNGfile,'w') as fp:  # clean file
                    pass 
            except Exception, e:
                if DEBUG:
                    print e
                else: 
                    pass  
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, m.as_string())
    server.quit()
    return 0
 
def updateMessage():
    messageFile=open(TEXT_File,'w')
    messageFile.write('Daily temperature report on %s at %s:\n'
        % (time.strftime('%A'), time.strftime('%H:%M')))
    messageFile.write('               current   min  max \n')
    for box in xbeeboxobjects:
        for Object in box.tempsensorobjects:
            try:
                messageFile.write('     %s:        %d F   %d F   %d F\n'
                    % (Object.name, Object.current, Object.minTemp, Object.maxTemp))
            except Exception as e:
                if DEBUG:
                    print e.message
        try:
            messageFile.write('Your %s power is {0:.2f} Volts. \n'
                .format(box.current) % box.name)
        except Exception as e:
            if DEBUG:
                print e.message
    messageFile.close()
    if DEBUG:
        print 'Today\'s update message sent' 
        
def updateMessage2():
    s = PrettyTable(['Loc','Cur','Min', 'Max'])
    messageFile=open(TEXT_File,'w')
    messageFile.write('Daily temperature report on %s at %s:\n' 
        % (time.strftime('%A'), time.strftime('%H:%M')))
    #s.add_row(['Garden', '','',''])
    #for Object in Garden_Objects:
        #try:
            #s.add_row([Object.DeviceLocation, Object.current, Object.minTemp, Object.maxTemp])
        #except Exception as e:
            #if DEBUG:
                #print e.message
    s.add_row(['House', '---','---','---'])
    for box in xbeeboxobjects:
        if box.name in ['Laundry', 'Kitchen', 'Garage']:
            for Object in box.tempsensorobjects:   
                try:
                    s.add_row([box.name+'_'+Object.name,'','',''])
                    s.add_row(['',Object.current, Object.minTemp, Object.maxTemp])
                        ## reset min and max temp
                    Object.minTemp=Object.current
                    Object.maxTemp=Object.current
                except Exception as e:
                    if DEBUG:
                        print e.message
    messageFile.write(s.get_string())
    messageFile.write("\n") 
    for box in xbeeboxobjects:
        try:
            messageFile.write('Your {0} power is {1:3.2f} Volts. \n'
                .format(box.name, box.current)) 
        except Exception as e:
            if DEBUG:
                print e.message
    messageFile.close()
    if DEBUG:
        print 'Today\'s update message sent'
                    
def createObjects(csvdict):
    # instantiate xbeeboxobjects and add to list
    xbeeboxobjects=[]
    for i in range(0,len(csvdict['xbeeboxlist'])):
        if csvdict['xbeeboxlist'][i]['boxname']!=None:
            xbeeboxobjects.append(XbeeBox(csvdict['xbeeboxlist'][i]) )
    # create groupings
    TEMP_OBJECTS=[]
    if DEBUG:
        for box in xbeeboxobjects:
            print (box.__dict__)
            print
            for probe in box.tempsensorobjects:
                print (probe.__dict__)
            print
    return xbeeboxobjects
            
def GetCSVDictionary(inputfile='datainput.csv'):
    #csv keys: boxname,xbeeID,tempprobe#,tempprobename,tempmin,tempmax
    csvdict={'xbeeboxlist':[]} # initiate dictionary
    with open(inputfile,'r') as csvfile:
        datainput=csv.DictReader(csvfile)
        for row in datainput:
            print row
            if row["boxname"]:      # new box
                csvdict['xbeeboxlist'].append({'boxname':row["boxname"]})
                ### add dictionary data to last box added to box list ###
                csvdict['xbeeboxlist'][-1]['tempprobelist']=[]
                csvdict['xbeeboxlist'][-1]['xbeeID']=ast.literal_eval(row["xbeeID"]) # this prevents escaping escape character (\)
                #if row['posttel']:
                csvdict['xbeeboxlist'][-1]['posttel']=row['posttel']    
                ##                          
                if row['tempprobename']:
                    csvdict['xbeeboxlist'][-1]['tempprobelist'].append({'probename':row["tempprobename"]})
                    ### add dictionary data to last temp probe added to temp probe list ###
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['probenumber']=int(row["tempprobe#"])
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['tempmin']=int(row["tempmin"])
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['tempmax']=int(row["tempmax"])
                    if (row["correction"]):
                        csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['correction']=int(row["correction"])
                    else:
                        csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['correction']=0
            else:                   # more data for same box
                if row['tempprobename']:
                    csvdict['xbeeboxlist'][-1]['tempprobelist'].append({'probename':row["tempprobename"]})
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['probenumber']=int(row["tempprobe#"])
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['tempmin']=int(row["tempmin"])
                    csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['tempmax']=int(row["tempmax"])
                    if (row["correction"]):
                        csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['correction']=int(row["correction"])
                    else:
                        csvdict['xbeeboxlist'][-1]['tempprobelist'][-1]['correction']=0

    if DEBUG:
        print csvdict
    return csvdict

def checkUpdateTime(today):
    if int(time.strftime('%H'))==0:
        for box in xbeeboxobjects:
            for sensor in box.tempsensorobjects:
                sensor.resetAlertTime() 
            box.resetAlertTime()        # battery 
    if int(time.strftime('%d'))!=today and int(time.strftime('%H')) >= UPDATE_TIME:
        updateMessage2()
        today=int(time.strftime('%d'))  # %d is day of month (decimal 1-31) 
        email('Today\'s Update', email_address)
        clearDataFiles()  
        for box in xbeeboxobjects:
            for sensor in box.tempsensorobjects:
                sensor.resetMinMax        

    return today
                
def main():
    global xbeeboxobjects

    #GetCSVDictionary()
    xbeeboxobjects=createObjects(GetCSVDictionary(INPUT_FILE))
    clearDataFiles()
    #parse_response({'source_addr_long': '\x00\x13\xa2\x00@\x89\xdf\x87', 'source_addr': '\x14\x1b', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 364, 'adc-1': 423, 'adc-2': 459, 'adc-7': 2616}], 'options': 'A'})
    print ('These are my xbee box objects: {0}'
            .format(xbeeboxobjects))
    # so we can look for change in file later       
    md5sumOld = subprocess.check_output('md5sum {0}'.format(INPUT_FILE), shell=True) 
    md5sumOld = md5sumOld.split(' ')[0]
    md5sumOldFetch=subprocess.check_output('md5sum {0}'.format(FETCH_REQUEST_FILE), shell=True) 
    md5sumOldFetch = md5sumOldFetch.split(' ')[0]
    if DEBUG:
        print md5sumOld
    # initiate xbee #
    ## replaced by udev rule to sym link coordinator to /dev/xbeesensors
    #try:
        #USBports=(subprocess.check_output("ls /dev/ttyUSB*", shell=True))
        #USBports=USBports.split('\n') # last port in list is ""
        #PORT=USBports[-2] 

    #except Exception as e:
        #if DEBUG:
            #print e.message
        #PORT=None
    print 'Initiating startup sequence for Sensor Network at %s:%s.' % (time.strftime('%H'), time.strftime('%M'))
    ser=serial.Serial(PORT, BAUD_RATE)  # Open serial port
    ser.flush() # flush port
    xbee=ZigBee(ser,escaped=True, callback=parse_response, error_callback=xbee_error) # asynchronous -> when serial data callback function initiated with response
    today=int(time.strftime('%d'))
    while True:
        try:
            time.sleep(SENSOR_TIME)
            
            for box in xbeeboxobjects:
                for sensor in box.tempsensorobjects: 
                    check_data_time(sensor)
            today=checkUpdateTime(today)
            #see if data input file has changed
            md5sumNew = subprocess.check_output('md5sum {0}'.format(INPUT_FILE), shell=True)
            md5sumNew = md5sumNew.split(' ')[0]
            if md5sumNew != md5sumOld:  # file has changed
                md5sumOld = md5sumNew
                xbee.halt()             # pause data evaluation
                xbeeboxobjects=createObjects(GetCSVDictionary(INPUT_FILE)) # reread file and recreate objects
                xbee=ZigBee(ser,escaped=True, callback=parse_response, error_callback=xbee_error) # restart
            #check for fetch request
            md5sumNewFetch = subprocess.check_output('md5sum {0}'.format(FETCH_REQUEST_FILE), shell=True)
            md5sumNewFetch = md5sumNewFetch.split(' ')[0]
            if md5sumNewFetch != md5sumOldFetch:    # file has changed
                md5sumOldFetch = md5sumNewFetch
                print('email requested')
                updateMessage2()
                email('Update',email_address)
        except KeyboardInterrupt:
            print   ''
            print "Closing down" 
            xbee.halt();
            ser.flush();
            ser.close();
            quit();
    return 0
    
def xbee_error(e):
    print "Xbee Error"
    print e
        
class XbeeBox(object):          
    ''' each xbee sensor box is an object with name refering to location of sensor box '''
    def __init__(self,boxdict): 
            
        self.name=boxdict['boxname']
        self.xbeeID=boxdict['xbeeID']
        self.battery=self.name+'_battery'
        self.alertTime = 4          # for battery
        self.current=None           # battery voltage
        self.tempsensorobjects=[]   # instatiate a list of temp probe objects
        for i in range(0,len(boxdict['tempprobelist'])):
            self.tempsensorobjects.append(TempSensor(self, boxdict['tempprobelist'][i]))
        if boxdict['posttel']:
            self.posttel=PostTel(self,boxdict['posttel'])
        else:
            self.posttel=False
    ## Battery Functions ##
    def resetAlertTime(self):
        self.alertTime = 4
    def batteryCheck(self):
        if self.current < BATTERY_THRESHOLD:
            warning='low'
            cond1=AM_ALERT_TIME<=int(time.strftime('%H'))<PM_ALERT_TIME
            cond2=int(time.strftime('%H'))>=(self.alertTime+ALERT_FREQUENCY)
        # no alerts before specified time and no more frequently than specified frequency
            if cond1 and cond2: 
                alertMessage(self, warning)         
            if DEBUG:
                print ('Your {0} is getting low with a voltage reading of {1:.2f} volts.\n'
                    .format(self.name, self.current))
        else:
            if DEBUG:
                print "Battery ok" 
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
        
class TempSensor(XbeeBox, object):
    def __init__(self,box, tempdict):
        self.box = box                  # assigns the parent box object
        self.name=tempdict['probename']
        self.number=tempdict['probenumber']
        self.correction=tempdict['correction']
        ## Thresholds ##
        self.TempMinAlert=tempdict['tempmin']
        self.TempMaxAlert=tempdict['tempmax']
        ## daily extremes ##
        self.maxTemp = -100
        self.minTemp = 100
        self.alertTime = 4
        ## prepare for capturing multiple data points to average
        self.start=datetime.datetime.utcnow()
        self.datalist=[]
    def resetMinMax(self):
        self.maxTemp = -100
        self.minTemp = 100
    def minmaxCheck(self): 
        if self.current>self.maxTemp:
            self.maxTemp=self.current
        if self.current<self.minTemp:
            self.minTemp=self.current   
    def alertCheck(self):       # thresholds
         # no alerts before specified time and no more frequently than specified frequency
        cond1=AM_ALERT_TIME<=int(time.strftime('%H'))<PM_ALERT_TIME
        cond2=int(time.strftime('%H'))>=(self.alertTime+ALERT_FREQUENCY)
        if not cond1 or not cond2:
            return 0
        if self.current<self.TempMinAlert:          
            self.warning='cold'
            alertMessage(self)
            if DEBUG:
                print 'Your %s is too cold at %d degrees! ' % (self.name, self.current)           
        if self.current>self.TempMaxAlert:
            self.warning='hot'
            alertMessage(self)
            if DEBUG:
                print 'Your %s is too hot at %d degrees! ' % (self.name, self.current)
       
    
## no in use                 
class PostTel(XbeeBox, object):
    def __init__(self,box,posttel):
        self.box=box
        self.name=posttel

# not implemented yet
class GardenTel():
    def __init__(self):
        self.windSpeed = 0;
        self.windDirection = 0;
        self.soilMoisture = 0; 
        self.humidity = 0;  




if __name__ == '__main__':
    main()

