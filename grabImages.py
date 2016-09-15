#!/usr/bin/env python

import Tkinter as tkinter
import subprocess, json, re, sys
from math import floor
from time import sleep
from datetime import datetime
import os
import re


def readIpJsonFile(filename):
   fptr=open(filename)
   fdata=json.load(fptr)
   numCams=len(fdata['mcams'])
   mcamId=[]
   ipList=[]
   srch1=re.compile('rtsp')
   srch2=re.compile('media')
   for i in range(numCams):
      mcamId.append(fdata['mcams'][i]['id'])
      ipString=fdata['mcams'][i]['url']
      print ipString
      ind1=srch1.search(ipString)
      ind2=srch2.search(ipString)
      ipList.append(ipString[ind1.end()+3:ind2.start()-1])
   return (mcamId,ipList)

def downloadImages():
 
   filename = sys.argv[1]


   (mcamId,iplist)=readIpJsonFile(filename)

   print iplist

   for ctr,ip in enumerate(iplist):
      print('this ip is '+ip)
      command='oneshotimage'
      #subprocess.Popen(['curl', '-u', 'admin:admin -o',str(ctr)+'.jpg', 'http://' + ip + '/' + command])   
      temp='curl -u admin:admin -o images/mcam_'+str(ctr+1)+'.jpg http://' + ip + '/' + command
      print temp
      os.popen(temp)
