import numpy as np
import cv2
import subprocess
import os
#from matplotlib import pyplot as plt
import re
import improc_library
import urllib
from PIL import Image
import cStringIO

settings_fname=""
ip=""

degrees_per_hex_val=0.022059
max_pan_degrees=180
min_pan_degrees=-180
min_tilt_degrees=-155
max_tilt_degrees=65


zoom_ifov_multiplier=0.03598
zoom_fit_p1=-4.5545e-5
zoom_fit_p0=1.0131


 
campan = [0.0]
camtilt = [0.0]
camzoom = [0.0]
camfocus = [0]

#def sendCurlCommand(ip,command)
#   subprocess.Popen(['curl', '-u', 'admin:admin', '--output',settings_fnames[item],'http://' + iplist[item] + '/command/' + command])

def grabCamImageUrl(ip):

   #req=urllib.urlopen('http://'+ip+'/oneshotimage.jpg')
   #arr=np.asarray(bytearray(req.read()), dtype=np.uint8)
   #print arr
   #img=cv2.imdecode(arr,-1)
   #cv2.imshow('lalala',img)
   urllib.urlcleanup()
   URL='http://'+ip+'/oneshotimage.jpg'

   file = cStringIO.StringIO(urllib.urlopen(URL).read())
   img=Image.open(file)
   open_cv_image = np.array(img) 
   open_cv_image = open_cv_image[:, :, ::-1].copy() 

   print open_cv_image.shape
   return open_cv_image

def grabCamImage(ip,filename):
   #subprocess.Popen(['curl', '-u', 'admin:admin', '--output',filename,'http://' + ip + '/oneshotimage.jpg'])
   #os.popen(['curl', '-u', 'admin:admin', '--output',filename,'http://' + ip + '/oneshotimage.jpg'])
   

   os.popen('curl -u admin:admin --output '+filename+' http://' + ip + '/oneshotimage.jpg')
   #subprocess.Popen(['curl','-u','admin:admin','-o',filename,'http://'+ip+'/oneshotimage.jpg'])

   



def downloadImages(mcamIds,iplist,writepath):
   for ctr,ip in enumerate(iplist):
      print('this ip is '+ip)
      command='oneshotimage'
      temp='curl -u admin:admin -o '+writepath+'/mcam_'+str(mcamIds[ctr])+'.jpg http://' + ip + '/' + command
      print temp
      os.popen(temp)
   return

#command to use curl to launch http request with proper permission
def writePTZ_to_file(settings_fname,ip):
   command='inquiry.cgi?inq=ptzf'
   os.popen('curl -u admin:admin --output ' +settings_fname+' http://' + ip + '/command/' + command)
   #subprocess.Popen(['curl','-u','admin:admin','-o',settings_fname,'http://'+ip+'/command'+command])

def writeImagingSettings_to_file(settings_fname,ip):
   command='inquiry.cgi?inq=imaging'
   os.popen('curl -u admin:admin --output ' +settings_fname+' http://' + ip + '/command/' + command)
   #subprocess.Popen(['curl','-u','admin:admin','-o',settings_fname,'http://'+ip+'/command'+command])


def findBallDelta(img,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize):

   # cv2.imshow('image',img)
   centroids=[]
   numObjects=2
   centroids=improc_library.findCentroid(img,numObjects,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)
   x1=centroids[0]['x']
   print x1
   x2=centroids[1]['x']
   print x2
   y1=centroids[0]['y']
   print y1
   y2=centroids[1]['y']
   print y2
   magx=int((x1+x2)/2)
   ceny=int((y1+y2)/2)
   length=np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
   return (length)
   
def findCentroid(img,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize):

   # cv2.imshow('image',img)
   centroids=[]
   numObjects=2
   centroids=improc_library.findCentroid(img,numObjects,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)
   x1=centroids[0]['x']
   print x1
   x2=centroids[1]['x']
   print x2
   y1=centroids[0]['y']
   print y1
   y2=centroids[1]['y']
   print y2
   cenx=int((x1+x2)/2)
   ceny=int((y1+y2)/2)
   return (cenx,ceny)
   # img=cv2.GaussianBlur(img,(5,5),0)
   # hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   # lower_green=np.array([60, 128, 128])
   # upper_green=np.array([80, 255, 255])
   # mask=cv2.inRange(hsv,lower_green,upper_green)
   # res=cv2.bitwise_and(img,img,mask= mask)  
   # (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   # print "I found %d black shapes" % (len(cnts))
   # blobArea=[0]*len(cnts)

   # # loop over the contours
   # for ctr,c in enumerate(cnts):
      # # draw the contour and show it
      # cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
      # cv2.imshow("Image", img)
      # #cv2.waitKey(0)
      # M=cv2.moments(c)
      # #print M
      # #print('Contour area is '+str(cv2.contourArea(c)))
      # blobArea[ctr]=cv2.contourArea(c)
      # print('Blob area is '+ str(blobArea[ctr]))  
   # cv2.waitKey(0)
      
   # maxindex=np.argmax(blobArea)
   # bigC=cnts[maxindex]
   # M=cv2.moments(bigC)

   # cx=int(M['m10']/M['m00'])
   # cy=int(M['m01']/M['m00'])

   # #print M

   # #print('centroid x is '+str(cx)+' centroid y is '+str(cy))
   
   # (x,y),radius=cv2.minEnclosingCircle(bigC)
   # center=(int(x),int(y))
   # radius=int(radius)
   # cv2.circle(img,center,radius,(0,255,0),2)
   # print('center x is '+str(x)+' center y is '+str(y))           
   # return (x,y)

   
def convertPanToDegrees(inputhex):
   unsignedIntVal=int(inputhex,16)
   if (unsignedIntVal>=pow(2,15)):
      signedIntVal=unsignedIntVal-pow(2,16)
   else:
      signedIntVal=unsignedIntVal
   panDegrees=float(signedIntVal)*degrees_per_hex_val  
   if panDegrees>max_pan_degrees:
      print('Something is wrong, pan degree setting is out of range')
   if panDegrees<min_pan_degrees:
      print('Something is wrong, pan degree setting is out of range')
   print('camera pan is at '+str(panDegrees)+ ' degrees')
   return panDegrees

def convertPanToHex(inputdegrees):
   if(inputdegrees>max_pan_degrees):
      inputdegrees-=360
   if(inputdegrees<min_pan_degrees):
      inputdegrees+=360
   signedIntVal=inputdegrees/degrees_per_hex_val
   if (signedIntVal<0):
      signedIntVal+=pow(2,16)
   print('hexString is '+str(signedIntVal))
   hexString=change2padhex(signedIntVal)
   return hexString

def convertUnsignedToSigned(inputhex):
   
   unsignedIntVal=int(inputhex,16)
   if (unsignedIntVal>=pow(2,15)):
      signedIntVal=unsignedIntVal-pow(2,16)
   else:
      signedIntVal=unsignedIntVal
   return signedIntVal      
   
def convertTiltToDegrees(inputhex):
   unsignedIntVal=int(inputhex,16)
   if (unsignedIntVal>=pow(2,15)):
      signedIntVal=unsignedIntVal-pow(2,16)
   else:
      signedIntVal=unsignedIntVal
   tiltDegrees=float(signedIntVal)*degrees_per_hex_val  
   if tiltDegrees>max_pan_degrees:
      print('Something is wrong, pan degree setting is out of range')
   if tiltDegrees<min_tilt_degrees:
      print('Something is wrong, pan degree setting is out of range')
   print('camera tilt is at '+str(tiltDegrees)+ ' degrees')
   return tiltDegrees
   
def convertTiltToHex(inputdegrees):
   signedIntVal=inputdegrees/degrees_per_hex_val
   print('tilt hex string is '+str(signedIntVal))
   hexString=change2padhex(signedIntVal)
   return hexString
   
def convertZoomToIfov(inputhex):
   print inputhex
   zoomInt=int(inputhex,16)
   print 'zoom int is'
   print str(zoomInt)

   
   iFov=zoom_ifov_multiplier/(pow(zoomInt*zoom_fit_p1+zoom_fit_p0,-2.5))
   print iFov
   return(iFov)
   

   
def convertIfovToZoom(iFov):
   reg=(pow(zoom_ifov_multiplier/iFov,-0.4)-zoom_fit_p0)/zoom_fit_p1
   print 'reg value is'
   print reg
   if reg>16384:
      reg=16384
      print('had to limit to 16384')
   if reg<1:
      reg=1
      print('had to limit to 1')
   hexString=change2padhex(reg)

   return hexString


def read_saved_ImagingSettings(settings_fname):
   camSettings=dict()
   pattern=re.compile("&")
   f = open(settings_fname)
   fileout=(f.read())
   
   fileChunk=fileout
   findAllOut=re.findall(pattern,fileout)
   #print len(findAllOut)
   #print 'length is above'
   for ii in range(len(findAllOut)+1):

      if ii<len(findAllOut):
         out=pattern.search(fileChunk)
      
         #print 'here now'
         #print out.start
         temp=fileChunk[0:out.start()]
         #print temp
      else:
         temp=fileChunk
   
      patternEq=re.compile("=")
      findEq=patternEq.search(temp)
      fieldName=temp[0:findEq.start()]
      fieldVal=temp[findEq.start()+1:len(temp)]
      #print fieldName
      #print fieldVal
      camSettings[fieldName]=fieldVal
      fileChunk=fileChunk[out.start()+1:len(fileChunk)]
      #print fileChunk
   


   f.close()


   return camSettings
   #f = open(settings_fname)
   #fileout=(f.read())
   #out=pattern.search(fileout)
   #item=0
   #if (out == None):
   #   print('Cant find PTZF')
   #else:
   #   ptzstart=out.start()+5
   #   temp=fileout[ptzstart:ptzstart+4]
   #   #campan[item]=int(temp,16)
   #   campan[item]=convertPanToDegrees(temp)
   #   temp=fileout[ptzstart+5:ptzstart+9]
   #   #camtilt[item]=int(temp,16)
   #   camtilt[item]=convertTiltToDegrees(temp)
   #   temp=fileout[ptzstart+10:ptzstart+14]
   #   #camzoom[item]=int(temp,16)
   #   camzoom[item]=convertZoomToIfov(temp)
   #  camzoomreg=convertIfovToZoom(camzoom[item])
   #   print('converted back to reg it is '+str(camzoomreg))
   #   temp=fileout[ptzstart+15:ptzstart+19]
   #   camfocus[item]=int(temp,16)
   #   print('pan is ' + str(campan[item]) + ' tilt is '+ str(camtilt[item])+' zoom is '+str(camzoom[item])+' focus is ' + str(camfocus[item]))
   #return(campan,camtilt,camzoom,camfocus)

def read_saved_PTZF(settings_fname):
   pattern=re.compile("PTZF")
   f = open(settings_fname)
   fileout=(f.read())
   out=pattern.search(fileout)
   item=0
   if (out == None):
      print('Cant find PTZF')
   else:
      ptzstart=out.start()+5
      temp=fileout[ptzstart:ptzstart+4]
      #campan[item]=int(temp,16)
      campan[item]=convertPanToDegrees(temp)
      temp=fileout[ptzstart+5:ptzstart+9]
      #camtilt[item]=int(temp,16)
      camtilt[item]=convertTiltToDegrees(temp)
      temp=fileout[ptzstart+10:ptzstart+14]
      #camzoom[item]=int(temp,16)
      camzoom[item]=convertZoomToIfov(temp)
      camzoomreg=convertIfovToZoom(camzoom[item])
      print('converted back to reg it is '+str(camzoomreg))
      temp=fileout[ptzstart+15:ptzstart+19]
      camfocus[item]=int(temp,16)
      print('pan is ' + str(campan[item]) + ' tilt is '+ str(camtilt[item])+' zoom is '+str(camzoom[item])+' focus is ' + str(camfocus[item]))
   return(campan,camtilt,camzoom,camfocus)

def read_saved_PTZF_string(settings_fname):
   pattern=re.compile("PTZF")
   f = open(settings_fname)
   fileout=(f.read())
   out=pattern.search(fileout)
   item=0
   if (out == None):
      print('Cant find PTZF')
   else:
      ptzstart=out.start()+5
      temp=fileout[ptzstart:ptzstart+4]
      #campan[item]=int(temp,16)
      campan=convertUnsignedToSigned(temp)
      #campan=(temp)
      temp=fileout[ptzstart+5:ptzstart+9]
      #camtilt[item]=int(temp,16)
      #camtilt=(temp)
      camtilt=convertUnsignedToSigned(temp)
      temp=fileout[ptzstart+10:ptzstart+14]
      #camzoom[item]=int(temp,16)
      #camzoom=(temp)
      camzoom=convertUnsignedToSigned(temp)
      #camzoomreg=convertIfovToZoom(camzoom[item])
      #print('converted back to reg it is '+str(camzoomreg))
      temp=fileout[ptzstart+15:ptzstart+19]
      camfocus=(temp)
      print('pan is ' + str(campan) + ' tilt is '+ str(camtilt)+' zoom is '+str(camzoom)+' focus is ' + str(camfocus))
   return(campan,camtilt,camzoom,camfocus)

   
def get_PTZF(settings_fname,ip):
   writePTZ_to_file(settings_fname,ip)
   pattern=re.compile("PTZF")
   f = open(settings_fname)
   fileout=(f.read())
   out=pattern.search(fileout)
   item=0
   if (out == None):
      print('Cant find PTZF')
   else:
      ptzstart=out.start()+5
      temp=fileout[ptzstart:ptzstart+4]
      #campan[item]=int(temp,16)
      campan[item]=convertPanToDegrees(temp)
      temp=fileout[ptzstart+5:ptzstart+9]
      #camtilt[item]=int(temp,16)
      camtilt[item]=convertTiltToDegrees(temp)
      temp=fileout[ptzstart+10:ptzstart+14]
      #camzoom[item]=int(temp,16)
      camzoom[item]=convertZoomToIfov(temp)
      camzoomreg=convertIfovToZoom(camzoom[item])
      print('converted back to reg it is '+str(camzoomreg))
      temp=fileout[ptzstart+15:ptzstart+19]
      camfocus[item]=int(temp,16)
      print('pan is ' + str(campan[item]) + ' tilt is '+ str(camtilt[item])+' zoom is '+str(camzoom[item])+' focus is ' + str(camfocus[item]))
   return(campan,camtilt,camzoom,camfocus)

         
def changePTZFCallBack(ip,newpan,newtilt,newzoom,newfocus):
   item=0
   #newzoomhex=change2padhex(newzoom)
   newzoomhex=convertIfovToZoom(newzoom)
   #newpanhex=change2padhex(newpan)
   newpanhex=convertPanToHex(newpan)
   #newtilthex=change2padhex(newtilt)
   newtilthex=convertTiltToHex(newtilt)
   newfocushex=change2padhex(newfocus)
#   command='ptzf.cgi?AbsolutePTZF='+newpanhex+','+newtilthex+','+newzoomhex+','+newfocushex
#   print(command)
   #subprocess.Popen(['./curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
   
   command='ptzf.cgi?AbsolutePanTilt='+newpanhex+','+newtilthex+','+str(12)+'&AbsoluteZoom='+newzoomhex
   

   print('new call back is'+'curl -u admin:admin http://'+ ip+'/command/'+command)
   
   #os.popen('curl -u admin:admin http://'+ ip+'/command/'+command)

   subprocess.Popen(['curl','-u','admin:admin','http://'+ip+'/command/'+command])


   #command='ptzf.cgi?AbsoluteZoom='+newzoomhex
   

   #subprocess.Popen(['curl','-u','admin:admin','http://'+ip+'/command/'+command])


         
def change2padhex(stringin):
   #print('in hex is '+hex(stringin))
   temp=hex(int(stringin))
   qq=len(temp)
   #print('length is '+str(qq))
   hexstring=''
   for i in range(qq,6):
      hexstring=hexstring+'0'
   for i in range(2,qq):
      #print(temp[i]+' i  is '+str(i))
      hexstring=hexstring+temp[i]
   return hexstring

def findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny):
   if (cenx>=imagecenterx):
      print('ball is right of center')
      newpan=campan[0]+panstep
   else:
      print('ball is left of center')
      newpan=campan[0]-panstep
   
   if (imagecentery>=ceny):
      print('ball is above center')
      newtilt=camtilt[0]+tiltstep
   else:
      print('ball is below center')
      newtilt=camtilt[0]-tiltstep
   return (newpan,newtilt)

def centerCamOnClick(ip,point_filename,settings_fname,x,y):

   print ip
   print point_filename
   print settings_fname

   #img=
   img=grabCamImageUrl(ip)

   #cv2.imread(point_filename)


   (height,width) = img.shape[:2]
   print('image width is '+str(width)+' image height is '+str(height))

   imagecenterx=width/2
   imagecentery=height/2


   print 'inside camclick x is' +str(x)
   print 'inside camclick y is' +str(y)

   #(cenx,ceny)=findCentroid(img,HueLowLimit,HueHighLimit,SatLowLimit)

   (campan,camtilt,camzoom,camfocus)=get_PTZF(settings_fname,ip)
   cenx=x
   ceny=y
   errorx=cenx-imagecenterx
   errory=ceny-imagecentery
   #errors.append([errorx,errory])
   print('image is off '+str(cenx-imagecenterx)+' in x and '+str(ceny-imagecentery)+' in y')
   panstep=1.0*(abs(cenx-imagecenterx))*camzoom[0]
   tiltstep=1.0*(abs(ceny-imagecentery))*camzoom[0]
   print(' pan step is '+str(panstep))
   print('tiltstep is '+str(tiltstep))
   (newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
   changePTZFCallBack(ip,newpan,newtilt,camzoom[0],camfocus[0])



   return 


def centerCams(iplist,point_filenames,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize):

   errors=[]
   
   for ctr,ip in enumerate(iplist):
      grabCamImage(ip,point_filenames[ctr])




   for ctr,ip in enumerate(iplist):
      print (point_filenames[ctr])
      img=cv2.imread(point_filenames[ctr])
      (height,width) = img.shape[:2]
      print('image width is '+str(width)+' image height is '+str(height))

      imagecenterx=width/2
      imagecentery=height/2




      (cenx,ceny)=findCentroid(img,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)

      (campan,camtilt,camzoom,camfocus)=get_PTZF(point_filenames[ctr],ip)

      errorx=cenx-imagecenterx
      errory=ceny-imagecentery
      errors.append([errorx,errory])
      print('image is off '+str(cenx-imagecenterx)+' in x and '+str(ceny-imagecentery)+' in y')
      panstep=0.75*(abs(cenx-imagecenterx))*camzoom[0]
      tiltstep=0.75*(abs(ceny-imagecentery))*camzoom[0]
      print(' pan step is '+str(panstep))
      print('tiltstep is '+str(tiltstep))
      (newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
      changePTZFCallBack(ip,newpan,newtilt,camzoom[0],camfocus[0])


   return errors

def optZoomCams(iplist,point_filenames,HueLowLimit,HueHighLimit,SatLowLimit,zoomTarget,ballSearchSize):
   
   errors=[]
   delta_ref=0
   for ctr,ip in enumerate(iplist):
      grabCamImage(ip,point_filenames[ctr])


   

   for ctr,ip in enumerate(iplist):
      print (point_filenames[ctr])
      img=cv2.imread(point_filenames[ctr])
      (height,width) = img.shape[:2]
      print('image width is '+str(width)+' image height is '+str(height))

      imagecenterx=width/2
      imagecentery=height/2

      delta_ref=height*zoomTarget/100
      


      delta=findBallDelta(img,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)
      print ('delta for ' + str(ip) +' is ' + str(delta))
      (campan,camtilt,camzoom,camfocus)=get_PTZF(point_filenames[ctr],ip)
      print('zoom is at '+str(camzoom[0]))
      #if (ctr==0):
      #   delta_ref=delta
      zoomerror=delta/delta_ref

      print ('zoom error is '+str(zoomerror))
      #if too big, zoomerror=2, ifov needs to decrease, new zoom=zoom/zoomerror
      newzoom=camzoom[0]*zoomerror
      print('new zoom is '+str(newzoom))
      changePTZFCallBack(ip,campan[0],camtilt[0],newzoom,camfocus[0])
      errors.append(zoomerror)
      #errorx=cenx-imagecenterx
      #errory=ceny-imagecentery
      #errors.append([errorx,errory])
      #print('image is off '+str(cenx-imagecenterx)+' in x and '+str(ceny-imagecentery)+' in y')
      #panstep=0.75*(abs(cenx-imagecenterx))*camzoom[0]
      #tiltstep=0.75*(abs(ceny-imagecentery))*camzoom[0]
      #print(' pan step is '+str(panstep))
      #print('tiltstep is '+str(tiltstep))
      #(newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
      #changePTZFCallBack(ip,newpan,newtilt,camzoom[0],camfocus[0])
   print ('zoom errors are ')
   print errors
   return 0



def centerCam(ip,filename,settings_fname,panstep,tiltstep,camzoom,camfocus,HueLowLimit,HueHighLimit,SatLowLimit):
   grabCamImage(ip,filename)





   img=cv2.imread(filename)
   (height,width) = img.shape[:2]
   print('image width is '+str(width)+' image height is '+str(height))

   imagecenterx=width/2
   imagecentery=height/2




   (cenx,ceny)=findCentroid(img,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)
   get_PTZF(settings_fname,ip)
   print('image is off '+str(cenx-imagecenterx)+' in x and '+str(ceny-imagecentery)+' in y')
   panstep=0.75*(abs(cenx-imagecenterx))*camzoom[0]
   tiltstep=0.75*(abs(ceny-imagecentery))*camzoom[0]
   print(' pan step is '+str(panstep))
   print('tiltstep is '+str(tiltstep))
   (newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
   changePTZFCallBack(ip,newpan,newtilt,camzoom[0],camfocus[0])



def change2padhex(stringin):
   #print('the string is '+str(stringin))
   temp=hex(int(stringin))
   qq=len(temp)
   #print('length is '+str(qq))
   hexstring=''
   for i in range(qq,6):
      hexstring=hexstring+'0'
   for i in range(2,qq):
      #print(temp[i]+' i  is '+str(i))
      hexstring=hexstring+temp[i]
   return hexstring

