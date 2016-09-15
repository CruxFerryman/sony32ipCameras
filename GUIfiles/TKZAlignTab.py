import Tkinter as tkinter
import tkFileDialog
import ttk
#import grabImages
import glob
import improc_library
import re
import cv2
import write_json_single_zone
import numpy as np
import sys
import json
import os
import write_json_multi_zone
import sony_ptz_library as sonyptz
from time import strftime
import subprocess
import socket
import shelve
import time


kb_left_arrow=1113937
kb_right_arrow=1113939
kb_escape=1048603
kb_enter=1113997

def createTKZtab(notebook,GUIglobals):
   TKZ = ttk.Frame(notebook)

   imageFilesPath=tkinter.StringVar(TKZ)

   Hmatpath=tkinter.StringVar(TKZ)
   numfiles_status=tkinter.StringVar(TKZ)
   iplist=[]
   mcamIds=[]
   imageFilenames=[]
   alignmentPoints=[]
   numAlignmentPoints=2
   Hmat=[]

   HueLowLimit=tkinter.IntVar(TKZ)
   HueHighLimit=tkinter.IntVar(TKZ)
   SatLowLimit=tkinter.IntVar(TKZ)
   zoomSizeTarget=tkinter.IntVar(TKZ)
   ballSearchSize=tkinter.IntVar(TKZ)
   zoom = tkinter.IntVar(TKZ)
   zoom.set(0)

   settings_path='settings_files/'
   settings_fname=settings_path+'ptzsettings0.txt'
 
   settings_fnames=[]

   default_save_dir='D:/Duke/Sony/cameraData/'
   state_fname='D:/Duke/Sony/cameraData/state1.txt'

   font=cv2.FONT_HERSHEY_SIMPLEX
   campan = [0.0]
   camtilt = [0.0]
   camzoom = [0.0]
   camfocus = [0]
   
   ip='10.1.201.242'
   point_path='images/temp'
   point_filenames=[]
   point_image_filenames=[]

   maxZones=20

   zoneZoomChoices={
      '1': '1',
      '2': '2',
      '3': '3',
   }


   zoneXChoices={
      '-2': '-2',
      '-1': '-1',
      '0': '0',
      '1': '1',
      '2': '2',
   }

   zoneYChoices={
      '-2': '-2',
      '-1': '-1',
      '0': '0',
      '1': '1',
      '2': '2',
   }

   zoneZoomVar=[]

   zoneYVar=[]
   zoneXVar=[]
   zoneIds=[]
   zoneDataset=[]

   zonePaths=[]

   assignZoneButtons=[]
   loadZoneButtons=[]


   def grabImages(mcamIds,iplist):
      print('in grabImages callback')
      print iplist

      

      foldername=strftime("%Y%m%d/%H%M%S")
      writepath=default_save_dir+foldername 
      os.makedirs(writepath)

      sonyptz.downloadImages(mcamIds,iplist,writepath)
      #grabImages.readIpJsonFile
      getImageFilenames()


      imageFilesPath.set(writepath)
      disableZoneWrite()

      return 0

   def loadImages():
      print('in load images callback')
      out=tkFileDialog.askdirectory(initialdir=default_save_dir)
      #print(out)
      imageFilesPath.set(out)
      getImageFilenames()

   def getImageFilenames():
      #mcamIds=[]
      #imageFilenames=[]
      del mcamIds[:]
      del imageFilenames[:]
      
      glob_out=glob.glob(imageFilesPath.get()+'//mcam*.jpg')
      print ('path is '+imageFilesPath.get())
      numfiles=len(glob_out)
      print('Found '+str(numfiles)+' jpegs in directory')
      numfiles_status.set(str(numfiles)+' jpegs found')
      srch1=re.compile('mcam_')
      srch2=re.compile('.jpg')
      for ctr in range(numfiles):
         temp=glob_out[ctr]
         ind1=srch1.search(temp)
         ind2=srch2.search(temp)
         #print str(ind1.start()+5)
         #print str(ind2.start())
         mcamIds.append(int((temp[ind1.start()+5:ind2.start()])))
         imageFilenames.append(temp)
         #print temp
         #print imageFilenames[ctr]
         #print mcamIds[ctr]
      print mcamIds
      qq=np.argsort(mcamIds)
      mcamIds_sort=[]
      imageFilenames_sort=[]
      for ctr in range(numfiles):
         print qq[ctr]
         print mcamIds[qq[ctr]]
         mcamIds_sort.append(mcamIds[qq[ctr]])
         imageFilenames_sort.append(imageFilenames[qq[ctr]])
         #print mcamIds_sort[ctr]
         #   print 'yo'
         #   print mcamIds[qq[ctr]]
         #   print 'ma'
         #   mcamIds_sort[ctr]=mcamIds[qq[ctr]]
      #mcamIds=mcamIds_sort
      #imageFilenames=imageFilenames_sort
      for ctr in range(numfiles):
         mcamIds[ctr]=mcamIds_sort[ctr]
         imageFilenames[ctr]=imageFilenames_sort[ctr]
      print mcamIds
      print imageFilenames
      return 0

   def findWarpTransform(iplist,settings_fnames):
      del Hmat[:]
      del alignmentPoints[:]
      #Below needs to be put in a callback/function called find WarpTransform
      for files in imageFilenames:
         #path='c:\Users'
         #fname='mcam_'+str(i+1)+'.jpg'
         #print(path+fname)
         img=cv2.imread(files)
         #mCamId.append((i+1))
         #cv2.imshow('image',img)

         alignmentPoints.append(improc_library.findCentroid(img,numAlignmentPoints,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize))
         print files
         cv2.waitKey(0)
         
         print alignmentPoints
   
      #Hmat=improc_library.MakeWarpTransforms(alignmentPoints)
      Hmat.append(improc_library.MakeWarpTransforms(alignmentPoints))
      print ('just got back from call')
      #print Hmat
      print ('now here')
      #Find warpTransform done
      improc_library.writeWarpMat(imageFilesPath.get(),mcamIds,Hmat)

      Hmatpath.set(imageFilesPath.get())



      path=imageFilesPath.get()+"/"
      os.makedirs(path+"settings_files")
      for ctr in range(len(iplist)):
         writePTZ_to_file(iplist[ctr],path+settings_fnames[ctr])      
      enableZoneWrite()
      return 0

   def checkWarpTransform():
      #Below needs to be put in callback CheckWarpAlignment
      #print Hmat
      for jj in range(2):
         ctr=0
         for files in imageFilenames:
            #path='c:\Users'
            #fname=str(i+1)+'.jpg'
            #print(path+'\\'+fname)
            #img=cv2.imread(path+'\\'+fname)

            #cv2.imshow('image',img)

            #alignmentPoints.append(improc_library.findCentroid(img,numAlignmentPoints))

            #cv2.waitKey(0)
            #fname='mcam_'+str(i+1)+'.jpg'
            print('ctr is '+str(ctr))
            print Hmat
            
            img=cv2.imread(files)
            imgWarp=improc_library.checkHmatAlignment(img,Hmat[0][ctr])


            #cv2.waitKey(33)
            r = 1000.0 / imgWarp.shape[1]
            dim = (1000, int(imgWarp.shape[0] * r))
            resized = cv2.resize(imgWarp, dim, interpolation = cv2.INTER_AREA)
            cv2.putText(resized,files,(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,255)
            cv2.imshow("Warped", resized)



            #cv2.imshow('warped',imgWarp)
            cv2.waitKey(50)
            ctr=ctr+1
            cv2.waitKey(0)
      #End callback Check Warp Alignment
      return 0

   def writeOneZoneJsonFile():

      write_json_single_zone.writeOneZone(Hmatpath.get())

      return 0

   def writeMultiZoneJsonFile():
      write_json_multi_zone.writeMultiZone()


   def readIpJsonFile(filename):
      fptr=open(filename)
      fdata=json.load(fptr)
      numCams=len(fdata['mcams'])
      mcamId=[]
      ipList=[]
      srch1=re.compile('rtsp')
      srch2=re.compile('media')
      for i in range(numCams):
         ipString=fdata['mcams'][i]['url']
         print ipString
         ind1=srch1.search(ipString)
         ind2=srch2.search(ipString)
         currentIp=ipString[ind1.end()+3:ind2.start()-1]
        
         mcamId.append(fdata['mcams'][i]['id'])
         
         ipList.append(ipString[ind1.end()+3:ind2.start()-1])
      return (mcamId,ipList)



   if len(sys.argv) == 1:
      filename = 'example.json'
   else:
      filename = sys.argv[1]

   def pointPTZCams(iplist,point_filenames):
      
      #(mcamId,iplist)=readIpJsonFile(filename)

      #ip=iplist[0]

      #sonyptz.grabCamImage(ip,point_filename)

      #img=cv2.imread(point_filename)
      #(height,width) = img.shape[:2]
      #print('image width is '+str(width)+' image height is '+str(height))

      #imagecenterx=width/2
      #imagecentery=height/2

      #(cenx,ceny)=sonyptz.findCentroid(img,HueLowLimit,HueHighLimit,SatLowLimit)

      #print('centroid x is ' +str(cenx)+' centroid y is '+str(ceny))
 
      #print settings_fname

      #(campan,camtilt,camzoom,camfocus)=sonyptz.get_PTZF(settings_fname,ip)

      #print('getting back to campan ')
      #print campan

      #panstep=100*camzoom[0]
      #tiltstep=100*camzoom[0]
      #sonyptz.centerCam(panstep,tiltstep)
      #sonyptz.centerCam(ip,point_filename,settings_fname,panstep,tiltstep,camzoom,camfocus,HueLowLimit,HueHighLimit,SatLowLimit)
      #(newpan,newtilt)=sonyptz.findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)

      errors=sonyptz.centerCams(iplist,point_filenames,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize)
      print 'errors are'
      print errors
      disableZoneWrite()
      #for ctr,ip in enumerate(iplist):
         #sonyptz.centerCam(ip,point_filename+str(ctr)+'.jpg',settings_fname,panstep,tiltstep,camzoom,camfocus,HueLowLimit,HueHighLimit,SatLowLimit)
       #  print('this ip is '+ip)

   def optZoomPTZCams(iplist,point_filenames):
      sonyptz.optZoomCams(iplist,point_filenames,HueLowLimit,HueHighLimit,SatLowLimit,zoomSizeTarget.get(),ballSearchSize)
      disableZoneWrite()
      return 0


         
   def writePTZ_to_file(ip,fname):
      command='inquiry.cgi?inq=ptzf'
      #curlcmd='curl -u admin:admin -o '+fname+' http://'+ip+'/command/'+command
      #subprocess.Popen(['curl', '-u', 'admin:admin', '-o ',fname,' http://' + ip + '/command/' + command])
      #m=(['curl', '-u', 'admin:admin', '-o ',fname,' http://' + ip + '/command/' + command])
      #subprocess.Popen([curlcmd])
      #os.popen(curlcmd)
      print fname
      print 'in write ptz'+ip+filename
      subprocess.Popen(['curl', '-u', 'admin:admin','-o',fname,'http://' + ip + '/command/' + command])



   def loadSavedPTZF(iplist,settings_fnames,zoneNum):
      path=default_save_dir+'zoneData/zone'+str(zoneNum)+'/'

      for ctr in range(len(iplist)):
         (campan,camtilt,camzoom,camfocus)=sonyptz.read_saved_PTZF(path+settings_fnames[ctr])
         print campan[0]
         sonyptz.changePTZFCallBack(iplist[ctr],campan[0],camtilt[0],camzoom[0],camfocus[0])
         
   def savePTZF(iplist,settings_fnames,zoneNum):
      print iplist

      path=default_save_dir+'zoneData/zone'+str(zoneNum)+'/'
      os.makedirs(path+'settings_files')
      for ctr in range(len(iplist)):
         writePTZ_to_file(iplist[ctr],path+settings_fnames[ctr])      
		
      return 0



   def changeZoomCallBack(iplist,point_filenames):
      #writePTZ_to_file('inquiry.cgi?inq=ptzf')
      print('in zoom call back  and zoom is at '+str(zoom.get()));   
      #items = map(int, lb.curselection())
      for ctr in range(len(iplist)):
         writePTZ_to_file(iplist[ctr], point_filenames[ctr]) 
         (campan,camtilt,camzoom,camfocus)=sonyptz.get_PTZF(point_filenames[ctr],iplist[ctr])     
         print('old zoom is at '+str(camzoom[0]))
         newzoom=zoom.get();
         print(str(hex(newzoom))+' in hex')
         newzoomhex=sonyptz.change2padhex(newzoom)
         command='ptzf.cgi?AbsoluteZoom='+newzoomhex
         print(command)
         subprocess.Popen(['curl', '-u', 'admin:admin', 'http://' + iplist[ctr] + '/command/' + command])

   def checkZoomZones():
      #print(zoneZoomVar[0].get())
      #print(zoneZoomVar[1].get())
      #print(zoneZoomVar[2].get())
      #print(zoneXVar[0].get())
      #print(zoneYVar[0].get())
      #print(zoneXVar[1].get())
      #print(zoneYVar[1].get())
      #print(zoneXVar[2].get())
      #print(zoneYVar[2].get())
      print assignZoneButtons
      
      assignZoneButtons[0].config(state=tkinter.NORMAL)

   def enableZoneWrite():
      for i in range(len(assignZoneButtons)):
         assignZoneButtons[i].config(state=tkinter.NORMAL)

   def disableZoneWrite():

      for i in range(len(assignZoneButtons)):
         assignZoneButtons[i].config(state=tkinter.DISABLED)

      

   def assignToZone(id):
      print(id)
      zoneDataset[id].set(imageFilesPath.get())
      imageFilesPath.get()
#      print zoneDataset[0].get()
#      print zoneDataset[1].get()
#      print zoneDataset[2].get()

      #assignZoneButtons[0].config(state='disabled')
      #print assignZoneButtons

   def shelveTkList(theshelf,thelocals,vname):
      temp=[]
      for i in thelocals[vname]:
         temp.append(i.get())
      theshelf[vname]=temp

   def unshelveTkList(theshelf,thelocals,vname):
      temp=[]
      for i in theshelf[vname]:
         temp.append(i)

      for ctr,i in enumerate(thelocals[vname]):
         i.set(temp[ctr])



   def saveState(gl):
      print gl
      my_shelf=shelve.open('/tmp/shelve.out','n')

      print gl['SatLowLimit']
      tt=gl['SatLowLimit']
      print tt.get()
      my_shelf['SatLowLimit']=gl['SatLowLimit'].get()
      print 'my shelf is'
      print my_shelf

      shelveTkList(my_shelf,gl,'zoneXVar')
      shelveTkList(my_shelf,gl,'zoneYVar')
      shelveTkList(my_shelf,gl,'zoneZoomVar')
      shelveTkList(my_shelf,gl,'zoneDataset')
      #my_shelf['zoneZoomVar']=gl['zoneZoomVar']

      #temp=gl['zoneZoomVar']
      #temp2=[]
      #for i in temp:
      #   #i=i.get() 
      #   temp2.append(i.get())
      #my_shelf['zoneZoomVar']=temp2
         
      #for key, value in gl.items():
      #   if not key.startswith('__'):
      #      try:
      #         my_shelf[key]=value
      #         print key
      #         print value
      #      except TypeError:
      #         print('ERROR shelving: {0}'.format(key))
      my_shelf.close()
      #print(globals())
      return 0
      

   def loadState(gl):
      my_shelf=shelve.open('/tmp/shelve.out')
      print my_shelf
      gl['SatLowLimit'].set(my_shelf['SatLowLimit'])
      unshelveTkList(my_shelf,gl,'zoneZoomVar')
      unshelveTkList(my_shelf,gl,'zoneXVar')
      unshelveTkList(my_shelf,gl,'zoneYVar')
      unshelveTkList(my_shelf,gl,'zoneDataset')
      #for key, value in my_shelf:
      #   gl[key]=my_shelf[key]
      #   print key
      #   print value
      my_shelf.close
      
      
      return 0

   def imagePathChecker(name, index, mode):
      getImageFilenames()
      print('dummy')

   def get_click(event,x,y,flags,param):
   #This function is called when a mouse click is done in the fine-tune cameras action
      if event==cv2.EVENT_LBUTTONDOWN:
         refPt=[(x,y)]
         print refPt
         print('just clicked')
         print param
         (ip,point_image_filename,settings_fname)=param
         print 'ip is'+str(ip)
         print 'filename is '+point_image_filename
         xcoord=1.92*float(x)
         ycoord=1.92*float(y)
         sonyptz.centerCamOnClick(ip,point_image_filename,settings_fname,xcoord,ycoord)


   def fineTuneCallback(iplist,point_image_filenames,settings_fnames):
      print point_image_filenames[0]

      
      current_image=0;
      #cv2.startWindowThread()
      
      a=0
      
      print('here')
      if (a==kb_enter):
         print('just pressed enter')

         print('just pressed escape')
      if (a==kb_left_arrow):
         print('just pressed left arrow')

         print('just pressed right arrow')
      cv2.namedWindow('FineTune', cv2.CV_WINDOW_AUTOSIZE)

      #cv2.startWindowThread()

      while(1):

         #sonyptz.grabCamImage(iplist[current_image],point_image_filenames[current_image])

         #time.sleep(0.2) 

         #img=cv2.imread(point_image_filenames[current_image])

         img=sonyptz.grabCamImageUrl(iplist[current_image])
           
         r = 1000.0 / img.shape[1]
         dim = (1000, int(img.shape[0] * r))
         resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
         cv2.putText(resized,'mcam_'+str(current_image),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
         cv2.putText(resized,'Click to center image',(0,100),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
         cv2.putText(resized,'Use L/R arrows to switch cameras',(0,150),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
         cv2.putText(resized,'Hit Esc to go back to GUI',(0,200),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)

         
         cv2.imshow('FineTune',resized)
         cv2.setMouseCallback('FineTune',get_click,(iplist[current_image],point_image_filenames[current_image],settings_fnames[current_image]))
         a=cv2.waitKey(1000)
         print('justpressed')
         print a
         if (a==kb_right_arrow):
            current_image=current_image+1
            if (current_image>(len(iplist)-1)):
               current_image=current_image-len(iplist)
         if (a==kb_left_arrow):
            current_image=current_image-1
            if (current_image<0):
               current_image=current_image+len(iplist)
         
         if (a==kb_escape):
            #cv2.destroyWindow('FineTune')
            cv2.waitKey(1)
            break

   imageFilesPath.trace("w",imagePathChecker)

   (mcamIds,iplist)=readIpJsonFile(filename)

   print mcamIds
   print iplist
 
   os.makedirs(point_path)
   for ids in mcamIds:
        settings_fnames.append(str('settings_files/ptzsettings'+str(ids)+'.txt'))
        point_filenames.append(point_path+'/ptzsettings'+str(ids)+'.txt')
        point_image_filenames.append(point_path+'/mcam_'+str(ids)+'.jpg')
        #print('item is ' + str(item))
        #   FOR TESTING:
        #print ['./curl', '-u', 'admin:admin', ' --output ',str(settingsdir.get()), ' http://' + iplist[item] + '/command/' + command]
        #print('./curl ' + ' -u ' + ' admin:admin ' + ' --output ' + str(settingsdir.get()) + '/ptzsettings' + str(item) + '.txt'   )
        #print(['./curl'])
   print('settings filenames are  ')
   print settings_fnames
   print('point filenames are ')
   print(point_filenames)

   tkinter.Button(TKZ, text="Grab New Images", command=lambda:grabImages(mcamIds,iplist)).grid(row=1,column=1,columnspan=1)
   tkinter.Button(TKZ, text="Load Saved Images", command=loadImages).grid(row=2,column=1,columnspan=1)
   tkinter.Label(TKZ, text="Path to current image files",textvariable=imageFilesPath).grid(row=3,column=1)
   tkinter.Label(TKZ, textvariable=numfiles_status).grid(row=4,column=1)
   tkinter.Button(TKZ, text="Find Warp Transform", command=lambda:findWarpTransform(iplist,settings_fnames)).grid(row=5,column=1,columnspan=1)
   tkinter.Button(TKZ, text="Check Warp Transform", command=lambda:checkWarpTransform()).grid(row=6,column=1,columnspan=1)
   tkinter.Button(TKZ, text="Export JSON File for Pursuit", command=lambda:writeOneZoneJsonFile()).grid(row=7,column=1,columnspan=1)
   tkinter.Button(TKZ, text="Export multi-zone JSON File for Pursuit", command=lambda:write_json_multi_zone.writeBigJson(zoneDataset,zoneXVar,zoneYVar,zoneZoomVar)).grid(row=8,column=1,columnspan=1)
   tkinter.Label(TKZ, text='Path to warp matrix', textvariable=Hmatpath).grid(row=9,column=1)
   


   # #Hue limit selection slider
   m = tkinter.Scale(TKZ, from_=20, to=100, orient=tkinter.HORIZONTAL, label="Hue Low Limit", variable=HueLowLimit )
   m.grid(row=1,column=2)
   m = tkinter.Scale(TKZ, from_=20, to=100, orient=tkinter.HORIZONTAL, label="Hue High Limit", variable=HueHighLimit )
   m.grid(row=2,column=2)
   HueLowLimit.set(30)
   HueHighLimit.set(90)
   m = tkinter.Scale(TKZ, from_=0, to=255, orient=tkinter.HORIZONTAL, label="Saturation Low Limit", variable=SatLowLimit )
   m.grid(row=3,column=2)
   SatLowLimit.set(50)
   # m.pack(padx=10, pady=10, fill=tkinter.X);
   


   tkinter.Button(TKZ, text="Point PTZ Cameras", command=lambda:pointPTZCams(iplist,point_filenames)).grid(row=5,column=2)
   tkinter.Button(TKZ, text="Optimize Zoom", command=lambda:optZoomPTZCams(iplist,point_filenames)).grid(row=6,column=2)

   m = tkinter.Scale(TKZ, from_=0, to=100, orient=tkinter.HORIZONTAL, label="Ball Search Size", variable=ballSearchSize )
   m.grid(row=7,column=2)
   ballSearchSize.set(100)

   tkinter.Button(TKZ, text="Save PTZ State 1", command=lambda:savePTZF(iplist,settings_fnames,1)).grid(row=11,column=1)
   tkinter.Button(TKZ, text="Save PTZ State 2", command=lambda:savePTZF(iplist,settings_fnames,2)).grid(row=12,column=1)
   tkinter.Button(TKZ, text="Save PTZ State 3", command=lambda:savePTZF(iplist,settings_fnames,3)).grid(row=13,column=1)
   tkinter.Button(TKZ, text="Save PTZ State 4", command=lambda:savePTZF(iplist,settings_fnames,4)).grid(row=14,column=1)
   tkinter.Button(TKZ, text="Save GUI State", command=lambda g=locals():saveState(g)).grid(row=15,column=1)

   tkinter.Button(TKZ, text="Load PTZ State 1", command=lambda:loadSavedPTZF(iplist,settings_fnames,1)).grid(row=11,column=2)
   tkinter.Button(TKZ, text="Load PTZ State 2", command=lambda:loadSavedPTZF(iplist,settings_fnames,2)).grid(row=12,column=2)
   tkinter.Button(TKZ, text="Load PTZ State 3", command=lambda:loadSavedPTZF(iplist,settings_fnames,3)).grid(row=13,column=2)
   tkinter.Button(TKZ, text="Load PTZ State 4", command=lambda:loadSavedPTZF(iplist,settings_fnames,4)).grid(row=14,column=2)
   tkinter.Button(TKZ, text="Load GUI State", command=lambda g2=locals():loadState(g2)).grid(row=15,column=2)



   for i in range(maxZones):

      zoneIds.append(i+1)
      zoneZoomVar.append(tkinter.StringVar(TKZ))
      zoneZoomOption=tkinter.OptionMenu(TKZ,zoneZoomVar[i],*zoneZoomChoices)
      zoneZoomOption.grid(row=1+i,column=3)
      zoneZoomVar[i].set('1')


      zoneXVar.append(tkinter.StringVar(TKZ))
      zoneXOption=tkinter.OptionMenu(TKZ,zoneXVar[i],*zoneXChoices)
      zoneXOption.grid(row=1+i,column=4)
      zoneXVar[i].set('0')

      zoneYVar.append(tkinter.StringVar(TKZ))
      zoneYOption=tkinter.OptionMenu(TKZ,zoneYVar[i],*zoneYChoices)
      zoneYOption.grid(row=1+i,column=5)
      zoneYVar[i].set('0')


      zoneDataset.append(tkinter.StringVar(TKZ))
      zoneDataset[i].set(i)
      #b=tkinter.Button(TKZ, text="Assign to zone "+str(i+1), state=tkinter.DISABLED, command=lambda ii=i:assignToZone(ii)).grid(row=1+i,column=6)
      #assignZoneButtons.append(b)

      #b=tkinter.Button(TKZ, text="Assign to zone "+str(i+1), state=tkinter.DISABLED, command=lambda ii=i:assignToZone(ii)).grid(row=1+i,column=6)
      assignZoneButtons.append(tkinter.Button(TKZ, text="Assign to zone "+str(i+1), state=tkinter.DISABLED, command=lambda ii=i:assignToZone(ii)))
      assignZoneButtons[i].grid(row=1+i,column=7)


      #assignZoneButtons.append(tkinter.Button(TKZ, text="Assign to zone "+str(i+1), command=assignToZone(i)).grid(row=1+i,column=6))
      tkinter.Label(TKZ, textvariable=zoneDataset[i]).grid(row=1+i,column=9)

      loadZoneButtons.append(tkinter.Button(TKZ, text="Load zone "+str(i+1), command=lambda ii=i:imageFilesPath.set(zoneDataset[ii].get())))
      loadZoneButtons[i].grid(row=i+1,column=8)

#   print b
   print assignZoneButtons

   #b.config(state=tkinter.NORMAL)

   print zoneIds
   tkinter.Label(TKZ, text="ZoneZoom").grid(row = 0, column = 3)

   tkinter.Label(TKZ, text="ZoneX").grid(row = 0, column = 4)


   tkinter.Label(TKZ, text="ZoneY").grid(row = 0, column = 5)

   #tkinter.Button(TKZ, text="Check Zoom Zones",command=lambda:checkZoomZones()).grid(row=10,column=3)
   
   # Zoom slider
   m = tkinter.Scale(TKZ, from_=0, to=16384, orient=tkinter.HORIZONTAL, label="Zoom Level", variable=zoom )
   #m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=17,column=1)
   tkinter.Button(TKZ, text="Change Zoom for All Cams", command = lambda:changeZoomCallBack(iplist,point_filenames)).grid(row=18,column=1)
   m = tkinter.Scale(TKZ, from_=0, to=100, orient=tkinter.HORIZONTAL, label="Zoom Size Target", variable=zoomSizeTarget )
   m.grid(row=18,column=2)
   zoomSizeTarget.set(50)

   tkinter.Button(TKZ, text="Fine Tune Cameras", command = lambda:fineTuneCallback(iplist,point_image_filenames,settings_fnames)).grid(row=19,column=1)

   return TKZ


