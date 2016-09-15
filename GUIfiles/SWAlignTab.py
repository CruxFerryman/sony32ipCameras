import Tkinter as tkinter
import subprocess, json, re, sys
from math import floor
from time import sleep
from datetime import datetime
import os
import re
import ttk
from time import strftime
import sony_ptz_library as sonyptz


#import GUIfiles.TKZAlignTab as TKZ

def createSWAtab(notebook,GUIglobals):
   SW = ttk.Frame(notebook)
   OPTIONS1 = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
   OPTIONS2 = ['-3', '-2', '-1', '0', '1', '2', '3']
   brightness = tkinter.StringVar(SW)
   brightness.set(OPTIONS1[int(len(OPTIONS1)/2)]) # default value
   saturation = tkinter.StringVar(SW)
   saturation.set(OPTIONS2[int(len(OPTIONS2)/2)]) # default value
   sharpness = tkinter.StringVar(SW)
   sharpness.set(OPTIONS2[int(len(OPTIONS2)/2)]) # default value
   contrast = tkinter.StringVar(SW)
   contrast.set(OPTIONS2[int(len(OPTIONS2)/2)]) # default value

   gain = tkinter.StringVar(SW)
   gain.set(7)
   expt = tkinter.StringVar(SW)
   expt.set(7)
   expseconds = tkinter.StringVar(SW)
   expseconds.set(0)
   iris = tkinter.StringVar(SW)
   iris.set(7)
   irisfsSW = tkinter.StringVar(SW)
   irisfsSW.set(0)
   wbcb = tkinter.IntVar(SW)
   wbcb.set(1000)
   wbcr = tkinter.IntVar(SW)
   wbcr.set(1000)
   settingsdir = tkinter.StringVar(SW)
   settingsdir.set('settings_files')
   zoom = tkinter.IntVar(SW)
   zoom.set(0)
   
   settings_fnames = ['blank.txt']*32
   campan = [0]*32
   camtilt = [0]*32
   camzoom = [0]*32
   camfocus = [0]*32
   
   if os.path.exists(str(settingsdir.get())) == True:
   	print('path exists')
   else:
   	os.makedirs(str(settingsdir.get()))
  
   #expoptions=['1/10000','1/5000','1/2000','1/1000','1/500','1/200','1/100','1/60','1/50','1/30','1/25','1/15','1/8','1/4','1/2','1']
   expoptions=['1/10000','1/6000','1/4000','1/3000','1/2000','1/1500','1/1000','1/725','1/500','1/350','1/250','1/180','1/125','1/100','1/90','1/60','1/30','1/15','1/8','1/4','1/2','1']
   
   irisoptions=['Close','f14','f11','f9.6','f8','f6.8','f5.6','f4.8','f4','f3.4','f2.8','f2.4','f2','f1.6']
   
   
   
   def autofocusCallBack():
      #curlIP('focuszoom.cgi?FzMove=focus,auto,0')
      #curlIP('system.cgi?DateFormat=ymd&GmTime=1503060750000&TimeZone=US/Pacific&DstMode=off&NtpService=off&NtpAuto=off')
      timestr=('15' + datetime.now().strftime('%m%d%H%M%S')+'0')
      print(timestr)
      curlIP('system.cgi?DateFormat=ymd&GmTime='+timestr+'&TimeZone=US/Pacific&DstMode=off&NtpService=off&NtpAuto=off')
      print('system.cgi?DateFormat=ymd&GmTime='+timestr+'&TimeZone=US/Pacific&DstMode=off&NtpService=off&NtpAuto=off')
      
      
      
      
   #initialize Camera to be in JPEG mode, 1920x1080 resolution, high-quality and to be in manual exposure
   def initcameraCallBack():
      curlIP('camera.cgi?ImageCodec1=jpeg&ImageSize1=1920,1080&FrameRate1=30&Quality1=3&JpBandWidth1=0&ImageCodec2=off&ImageCodec3=off&WideDynamicRangeLevel=level1');
      curlIP('imaging.cgi?ExposureMode=manual&WhiteBalanceMode=manual&VisibilityEnhancer=0');
      curlIP('system.cgi?DateFormat=ymd&TimeZone=US/Pacific&DstMode=off&NtpServer=10.1.200.140&NtpService=on&NtpAuto=off');
      
   def h264CallBack():
      curlIP('camera.cgi?ImageCodec1=h264');
   
   def CBRCallBack():
      curlIP('camera.cgi?CBR1=on');
      
   def VBRCallBack():
      curlIP('camera.cgi?CBR1=off');
      
   #callback to change the camera white balance settings using the Cb and Cr parameters
   def changecbCallBack():
      curlIP('imaging.cgi?WhiteBalanceCbGain=' + str(wbcb.get())+'&WhiteBalanceCrGain=' + str(wbcr.get()));
   
   #callback to change the exposure time and gain settings of the camera
   def changeExpCallBack():
      curlIP('imaging.cgi?ExposureExposureTime=' + expt.get()+'&ExposureGain=' + gain.get() + '&ExposureIris=' + iris.get());
   
   def changeZoomCallBack():
      writePTZ_to_file('inquiry.cgi?inq=ptzf')
      print('in zoom call back  and zoom is at '+str(zoom.get()));   
      items = map(int, lb.curselection())
      for item in items:
         print('old zoom is at '+str(camzoom[item]))
         newzoom=zoom.get();
         print(str(hex(newzoom))+' in hex')
         newzoomhex=change2padhex(newzoom)
         print('it returned '+(newzoomhex))
         oldpan=change2padhex(campan[item])
         print('old pan is '+oldpan)
         oldtilt=change2padhex(camtilt[item])
         print('old tilt is '+oldtilt)
         oldfocus=change2padhex(camfocus[item])
         print('old focus is '+oldfocus)
         command='ptzf.cgi?AbsolutePTZF='+oldpan+','+oldtilt+','+newzoomhex+','+oldfocus
         print(command)
         subprocess.Popen(['curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
   
   def goWideCallBack():
      print('gowide')
      curlIP('presetposition.cgi?PresetCall=1,24')
      
   def goTightCallBack():
      print('go tight')
      curlIP('presetposition.cgi?PresetCall=2,24')
      
   def setWideCallBack():
      print('set wide')
      curlIP('presetposition.cgi?PresetSet=1,Wide,off')
      
   def setTightCallBack():      
      print('set tight')
      curlIP('presetposition.cgi?PresetSet=2,Tight,off')
         
   def displayExpCallBack(val):
   #   print['exposure slider is at ',val]
      expseconds.set(expoptions[int(val)]+' second');
   
   def displayIrisCallBack(val):
   #   print['exposure slider is at ',val]
      irisfsSW.set(irisoptions[int(val)]);

   def readImagingSettings(imagingsettingsfile,ip):
      sonyptz.writeImagingSettings_to_file(imagingsettingsfile,ip)
      camSettings=sonyptz.read_saved_ImagingSettings(imagingsettingsfile)
            
      wbcb.set(int(camSettings[('WhiteBalanceCbGain')]))
     
      wbcr.set(int(camSettings[('WhiteBalanceCrGain')]))


      expt.set(int(camSettings['ExposureExposureTime']))
      gain.set(int(camSettings['ExposureGain']))
      iris.set(int(camSettings['ExposureIris']))

      brightness.set(OPTIONS1[int(camSettings['Brightness'])]) # default value

      saturation.set(OPTIONS2[int(camSettings['ColorSaturation'])]) # default value

      sharpness.set(OPTIONS2[int(camSettings['Sharpness'])]) # default value
      return
   
   def change2padhex(stringin):
      #print('in hex is '+hex(stringin))
      temp=hex(stringin)
      qq=len(temp)
      #print('length is '+str(qq))
      hexstring=''
      for i in range(qq,6):
         hexstring=hexstring+'0'
      for i in range(2,qq):
         #print(temp[i]+' i  is '+str(i))
         hexstring=hexstring+temp[i]
      return hexstring
      
   #callback for imaging settings for brightness, sharpness, contrast
   def submitCallBack():
      curlIP('imaging.cgi?Brightness=' + str(int(brightness.get()) + int((len(OPTIONS1)-1)/2)) + '&ColorSaturation=' + str(int(saturation.get()) + int((len(OPTIONS2)-1)/2)) + '&Sharpness=' + str(int(sharpness.get()) + int((len(OPTIONS2)-1)/2)) + '&Contrast=' + str(int(contrast.get()) + int((len(OPTIONS2)-1)/2)))
   
   def GrabColorCalCallback():
     # TKZ.grabImages()
      #print notebook
      #print TKZ.
      print GUIglobals

      current_iris=iris.get()

      foldername=strftime("%Y%m%d/%H%M%S")+'ColorCal'
      print current_iris
      print 'that was current_iris'
      for i in range(int(current_iris)):
         iris.set(i+1)

         writepath=GUIglobals['default_save_dir']+foldername+'/'+irisoptions[i+1] 
         os.makedirs(writepath)
         changeExpCallBack()
         sleep(5) 

         sonyptz.downloadImages(mcamIds,iplist,writepath)
         print 'im here' + str(i)
      return 0

   #command to use curl to launch http request with proper permission
   def curlIP(command):
      items = map(int, lb.curselection())
      for item in items:
           #subprocess.Popen(['/usr/bin/curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
           subprocess.Popen(['curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
           print('item is ' + str(item))
           #   FOR TESTING:
           #print ['./curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command]
   
   #command to use curl to launch http request with proper permission
   #to make this more general would need to be able to specify settings_fnames for the ptzf or for the imaging settings
   def writePTZ_to_file(command):
      items = map(int, lb.curselection())
      for item in items:
           #subprocess.Popen(['/usr/bin/curl', '-u', 'admin:admin', 'http://' + iplist[item] + '/command/' + command])
           subprocess.Popen(['curl', '-u', 'admin:admin', '--output',settings_fnames[item],'http://' + iplist[item] + '/command/' + command])
           print('item is ' + str(item))
           #   FOR TESTING:
           #print ['./curl', '-u', 'admin:admin', ' --output ',str(settingsdir.get()), ' http://' + iplist[item] + '/command/' + command]
           #print('./curl ' + ' -u ' + ' admin:admin ' + ' --output ' + str(settingsdir.get()) + '/ptzsettings' + str(item) + '.txt'   )
           #print(['./curl'])
   
   def check_Zoom():
      items = map(int, lb.curselection())
      pattern=re.compile("PTZF")
      for item in items:
         f = open(settings_fnames[item])
         fileout=(f.read())
         out=pattern.search(fileout)
         if (out == None):
            print('Cant find PTZF')
         else:
            ptzstart=out.start()+5
            temp=fileout[ptzstart:ptzstart+4]
            #campan[item]=10
            campan[item]=int(temp,16)
            temp=fileout[ptzstart+5:ptzstart+9]
            camtilt[item]=int(temp,16)
            temp=fileout[ptzstart+10:ptzstart+14]
            camzoom[item]=int(temp,16)
            temp=fileout[ptzstart+15:ptzstart+19]
            camfocus[item]=int(temp,16)
            print('pan is ' + str(campan[item]) + ' tilt is '+ str(camtilt[item])+' zoom is '+str(camzoom[item])+' focus is ' + str(camfocus[item]))
      zoom.set(camzoom[0])   
            
            
            		 
      
   		
   def selectAllHandler():
      if selectAllChecked.get() == True:
         lb.selection_set(0, tkinter.END)
      else:
         lb.selection_clear(0, tkinter.END)
   
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
         
   if len(sys.argv) == 1:
      filename = 'example.json'
   else:
      filename = sys.argv[1]
   
   (mcamIds,iplist)=readIpJsonFile(filename)

   imagingsettingsfile='imagingsettings.txt'



   camSettings=readImagingSettings(imagingsettingsfile,iplist[0])


   print 'Cam Settings are'
   print camSettings
   #json_data = open(filename)
   #data = json.load(json_data)
   #json_data.close()
   
   #iplist = []
   currow=0;
   
   #read camera list from supplied json file
   #for ip in data['mcams']:
   #   try:
   #      iplist.append(re.findall(r'[0-9]{1,3}(?:\.[0-9]{1,3}){3}', ip)[0])
   #   except IndexError:
   #      pass
   
   
   	  
   	  
   #tkinter.Button(SW, text="Autofocus", command = autofocusCallBack).pack(padx=10, pady=10, fill=tkinter.X)
   #tkinter.Button(SW, text="Init Camera", command = initcameraCallBack).pack(padx=10, pady=10, fill=tkinter.X)
   tkinter.Button(SW, text="Autofocus", command = autofocusCallBack).grid(row=currow,column=0)
   tkinter.Button(SW, text="Init Camera/JPEG Mode", command = initcameraCallBack).grid(row=currow,column=1)
   
   currow=currow+1
   
   
   tkinter.Button(SW, text="H264 Mode", command = h264CallBack).grid(row=currow,column=1)
   
   currow=currow+1
   
   # #White balance Cb selection slider
   m = tkinter.Scale(SW, from_=0, to=4095, orient=tkinter.HORIZONTAL, label="WhiteBal Cb", variable=wbcb )
   #m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=0);
   
   # #White balance Cr selection slider
   m = tkinter.Scale(SW, from_=0, to=4095, orient=tkinter.HORIZONTAL, label="WhiteBal Cr", variable=wbcr )
   # m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=1);
   
   currow=currow+1
   
   # #Button to apply white balance setting
   # tkinter.Button(SW, text="Apply WB", command = changecbCallBack).pack(padx=10, pady=10, fill=tkinter.X)
   tkinter.Button(SW, text="Apply WB", command = changecbCallBack).grid(row=currow,column=0)
   
   currow=currow+1
   
   # #Exposure time selection slider
   m = tkinter.Scale(SW, from_=0, to=22, orient=tkinter.HORIZONTAL, label="Exposure time", variable=expt, command=displayExpCallBack )
   # m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=0)
   
   # #Gain selection slider
   m = tkinter.Scale(SW, from_=0, to=10, orient=tkinter.HORIZONTAL, label="Gain", variable=gain )
   # m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=1)
   
   
   currow=currow+1
   
   tkinter.Label(SW, textvariable=expseconds).grid(row=currow,column=0)
   
   currow=currow+1
   
   # #Iris selection slider
   m = tkinter.Scale(SW, from_=0, to=13, orient=tkinter.HORIZONTAL, label="Iris", variable=iris, command=displayIrisCallBack )
   # m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=1)
   
   currow=currow+1
   
   tkinter.Label(SW, textvariable=irisfsSW).grid(row=currow,column=1)
   
   
   # #Button to apply exposure time and gain
   # tkinter.Button(SW, text="Apply Exposure/Gain", command = changeExpCallBack).pack(padx=10, pady=10, fill=tkinter.X)
   tkinter.Button(SW, text="Apply Exposure/Gain", command = changeExpCallBack).grid(row=currow,column=0)
   
   currow=currow+1
   
   w = tkinter.LabelFrame(SW, text="Select Cameras")
   #w.pack(padx=10, pady=10, fill='both', expand=True)
   w.grid(row=0,column=2,rowspan=5)
   scrollbar = tkinter.Scrollbar(w, orient="vertical")
   lb = tkinter.Listbox(w, selectmode=tkinter.MULTIPLE, yscrollcommand=scrollbar.set)
   scrollbar.config(command=lb.yview)
   scrollbar.grid(row=0,column=1,rowspan=5)
   # scrollbar.pack(side="right", fill="y")
   # #lb.pack(side="left",fill="y", expand=True)
   for ip in iplist:
   	lb.insert(tkinter.END, ip)
   	lb.grid(row=0,column=0,rowspan=5)
   	#lb.pack(fill='y', expand=True)
   
   	
   selectAllChecked = tkinter.BooleanVar()
   c = tkinter.Checkbutton(w, text="Select All", command=selectAllHandler, variable=selectAllChecked)
   #c.pack(side='left')
   c.grid(row=1,column=2)
   selectAllChecked.set(True)
   selectAllHandler()
   
   	
   w = tkinter.Scale(SW, from_=-5, to=5, orient=tkinter.HORIZONTAL, label="Brightness", variable=brightness)
   w.grid(row=currow,column=0)
   
   tkinter.Button(SW, text="Apply Brightness/Saturation.. Controls", command = submitCallBack).grid(row=currow,column=1,columnspan=1)
   
   
   # w.pack(padx=10, pady=10, fill=tkinter.X)
   # #m = apply(tkinter.OptionMenu, (w, brightness) + tuple(OPTIONS1))
   # m = tkinter.OptionMenu(SW, (w,brightness), tuple(OPTIONS1))
   # m.pack();
   
   currow=currow+1
   
   w= tkinter.Scale(SW, from_=-3, to=3, orient=tkinter.HORIZONTAL, label="Saturation", variable=saturation)
   w.grid(row=currow,column=0)
   
   tkinter.Button(SW, text="VBR Mode", command = VBRCallBack).grid(row=currow,column=1)
   
   
   # # w = tkinter.LabelFrame(SW, text="Saturation")
   # # w.pack(padx=10, pady=10, fill=tkinter.X)
   # # m = apply(tkinter.OptionMenu, (w, saturation) + tuple(OPTIONS2))
   # # m.pack();
   
   currow=currow+1
   
   w= tkinter.Scale(SW, from_=-3, to=3, orient=tkinter.HORIZONTAL, label="Sharpness", variable=sharpness)
   w.grid(row=currow,column=0)
   
   tkinter.Button(SW, text="CBR Mode", command = CBRCallBack).grid(row=currow,column=1)
   
   
   currow=currow+1
   
   w= tkinter.Scale(SW, from_=-3, to=3, orient=tkinter.HORIZONTAL, label="Contrast", variable=contrast)
   w.grid(row=currow,column=0)
   # # 
   # # w = tkinter.LabelFrame(SW, text="Sharpness")
   # # w.pack(padx=10, pady=10, fill=tkinter.X)
   # # m = apply(tkinter.OptionMenu, (w, sharpness) + tuple(OPTIONS2))
   # # m.pack();
   
   # # w = tkinter.LabelFrame(SW, text="Contrast")
   # # w.pack(padx=10, pady=10, fill=tkinter.X)
   # # m = apply(tkinter.OptionMenu, (w, contrast) + tuple(OPTIONS2))
   # # m.pack();
   currow=currow+1	
   
   tkinter.Button(SW, text="Grab Color Cal Data", command=GrabColorCalCallback).grid(row=currow,column=0)
   
   
   currow=7
   
   # Zoom slider
   m = tkinter.Scale(SW, from_=0, to=16384, orient=tkinter.HORIZONTAL, label="Zoom Level", variable=zoom )
   #m.pack(padx=10, pady=10, fill=tkinter.X);
   m.grid(row=currow,column=2);
   
   currow=currow+1
   tkinter.Button(SW, text="Change Zoom", command = changeZoomCallBack).grid(row=currow,column=2)
   currow=currow+1
   tkinter.Button(SW, text="Go Wide", command = goWideCallBack).grid(row=currow,column=2)
   currow=currow+1
   tkinter.Button(SW, text="Go Tight", command = goTightCallBack).grid(row=currow,column=2)
   currow=currow+1
   tkinter.Button(SW, text="Set Wide", command = setWideCallBack).grid(row=currow,column=2)
   currow=currow+1
   tkinter.Button(SW, text="Set Tight", command = setTightCallBack).grid(row=currow,column=2)
   
   	
   # selectAllChecked = tkinter.BooleanVar()
   # c = tkinter.Checkbutton(w, text="Select All", command=selectAllHandler, variable=selectAllChecked)
   # #c.pack(side='left')
   # c.grid(row=currow,column=0)
   # selectAllChecked.set(True)
   # selectAllHandler()
   
   
   items = map(int, lb.curselection())
   for item in items:
        settings_fnames[item]=str((settingsdir.get())+'/ptzsettings'+str(item)+'.txt')
        print('item is ' + str(item))
        #   FOR TESTING:
        #print ['./curl', '-u', 'admin:admin', ' --output ',str(settingsdir.get()), ' http://' + iplist[item] + '/command/' + command]
        #print('./curl ' + ' -u ' + ' admin:admin ' + ' --output ' + str(settingsdir.get()) + '/ptzsettings' + str(item) + '.txt'   )
        #print(['./curl'])
   print('first one is ' + settings_fnames[0])
   
   #This is the callback to get all of the current camera settings. Currently hard coded for ptzf (pan tilt zoom focus settings), to get imaging settings, use inq=imaging to get imaging settings needed to default the GUI to current camera parameters 
   writePTZ_to_file('inquiry.cgi?inq=ptzf')
   
   
   #check_Zoom()



   return SW
