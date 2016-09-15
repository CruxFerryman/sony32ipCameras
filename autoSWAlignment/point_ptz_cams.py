import numpy as np
import cv2
import subprocess
import os
#from matplotlib import pyplot as plt
import re
import improc_library.py

#def sendCurlCommand(ip,command)
#   subprocess.Popen(['curl', '-u', 'admin:admin', '--output',settings_fnames[item],'http://' + iplist[item] + '/command/' + command])

def grabCamImage(ip,filename):
   #subprocess.Popen(['curl', '-u', 'admin:admin', '--output',filename,'http://' + ip + '/oneshotimage.jpg'])
   #os.popen(['curl', '-u', 'admin:admin', '--output',filename,'http://' + ip + '/oneshotimage.jpg'])
   os.popen('curl -u admin:admin --output '+filename+' http://' + ip + '/oneshotimage.jpg')
   

#command to use curl to launch http request with proper permission
def writePTZ_to_file():
   command='inquiry.cgi?inq=ptzf'
   os.popen('curl -u admin:admin --output ' +settings_fname+' http://' + ip + '/command/' + command)
   
   
def findCentroid(img):

   # cv2.imshow('image',img)
   centroids=[]
   numObjects=2
   centroids=improc_library.findCentroid(img,numObjects)
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
   iFov=0.03598*np.polyval(zoom_fit_p,zoomInt)
   
   iFov=zoom_ifov_multiplier/(pow(zoomInt*zoom_fit_p1+zoom_fit_p0,-2.5))
   print iFov
   return(iFov)
   

   
def convertIfovToZoom(iFov):
   reg=(pow(zoom_ifov_multiplier/iFov,-0.4)-zoom_fit_p0)/zoom_fit_p1
   print 'reg value is'
   print reg
   hexString=change2padhex(reg)

   return hexString

   
def get_PTZF():
   writePTZ_to_file()
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
         
def changePTZFCallBack(newpan,newtilt,newzoom,newfocus):
   item=0
   #newzoomhex=change2padhex(newzoom)
   newzoomhex=convertIfovToZoom(newzoom)
   #newpanhex=change2padhex(newpan)
   newpanhex=convertPanToHex(newpan)
   #newtilthex=change2padhex(newtilt)
   newtilthex=convertTiltToHex(newtilt)
   newfocushex=change2padhex(newfocus)
   command='ptzf.cgi?AbsolutePTZF='+newpanhex+','+newtilthex+','+newzoomhex+','+newfocushex
   print(command)
   #subprocess.Popen(['./curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
   
   
   os.popen('curl -u admin:admin http://'+ ip+'/command/'+command)

         
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
   
def centerCam(panstep,tiltstep):
   grabCamImage(ip,filename)
   img=cv2.imread(filename)
   (cenx,ceny)=findCentroid(img)
   get_PTZF()
   print('image is off '+str(cenx-imagecenterx)+' in x and '+str(ceny-imagecentery)+' in y')
   panstep=0.75*(abs(cenx-imagecenterx))*camzoom[0]
   tiltstep=0.75*(abs(ceny-imagecentery))*camzoom[0]
   print(' pan step is '+str(panstep))
   print('tiltstep is '+str(tiltstep))
   (newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
   changePTZFCallBack(newpan,newtilt,camzoom[0],camfocus[0])


   
settings_fname='ptz0settings.txt'
 
degrees_per_hex_val=0.022059
max_pan_degrees=180
min_pan_degrees=-180
min_tilt_degrees=-155
max_tilt_degrees=65

zoom_fit_p=(-2.2097e-21,9.6885e-17,-1.5006e-12,1.2216e-8,-1.2314e-4,1)
zoom_ifov_multiplier=0.03598
zoom_fit_p1=-4.5545e-5
zoom_fit_p0=1.0131

 
campan = [0.0]
camtilt = [0.0]
camzoom = [0.0]
camfocus = [0]
   
#ip='10.1.201.222'
ip='10.1.201.201'
filename='temp.jpg'

grabCamImage(ip,filename)
   

img=cv2.imread(filename)
(height,width) = img.shape[:2]
print('image width is '+str(width)+' image height is '+str(height))

imagecenterx=width/2
imagecentery=height/2


(cenx,ceny)=findCentroid(img)

print('centroid x is ' +str(cenx)+' centroid y is '+str(ceny))

#Get current camera's PTZF 
get_PTZF()

panstep=100*camzoom[0]
tiltstep=100*camzoom[0]



(newpan,newtilt)=findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
#changePTZFCallBack(newpan,newtilt,camzoom[0],camfocus[0])



print('New pan is '+str(newpan)+' new tilt is '+str(newtilt))

centerCam(panstep,tiltstep)
##
panstep=50*camzoom[0]
tiltstep=50*camzoom[0]
##

#cv2.waitKey(0)
centerCam(panstep,tiltstep)
#cv2.waitKey(0)

centerCam(panstep,tiltstep)
#cv2.waitKey(0)

centerCam(panstep,tiltstep)


##
panstep=10*camzoom[0]
tiltstep=10*camzoom[0]
##
#centerCam(panstep,tiltstep)
#centerCam(panstep,tiltstep)
#centerCam(panstep,tiltstep)

##panstep=2
##tiltstep=2


#centerCam(panstep,tiltstep)
#centerCam(panstep,tiltstep)
#centerCam(panstep,tiltstep)

   



   
#dim=(480,270)

#img=cv2.resize(img,dim)

#(height,width) = img.shape[:2]

#height=height/4

#width=width/4

#print('height is '+str(height)+' width is'+str(width))

#dim=(width,height)


#res_ds=cv2.resize(res,dim)

#gray_result=cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

#hist=cv2.calcHist([gray_result],[0],None,[256],[0,256])

#plt.hist(gray_result.ravel(),256,[0,256]);plt.show()

#plt.plot(hist)
#plt.show()

# find the contours in the mask
#cv2.imshow("Mask", mask)
 
 

#cv2.waitKey(0)

#ret,thresh = cv2.threshold(gray_result,50,255,0)

#cv2.imshow('threshold',thresh)

#contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.imshow('threshold',gray_result)


#cv2.drawContours(gray_result, contours, -1,(0,255,0),3)

#cnt=contours[0]
#M=cv2.moments(cnt)

#print M

#cv2.imshow('img',img)
#cv2.imshow('mask',mask)
#cv2.imshow('res',res_ds)



cv2.destroyAllWindows()
