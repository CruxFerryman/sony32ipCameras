#ptz fields
import json
import numpy as np
import sony_ptz_library as sonyptz
from time import strftime
import os

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def writeBigJson(filepath,zoneXVar,zoneYVar,zoneZoomVar):


   #print zoneXVar
   #print zoneYVar
   #print zoneZoomVar

   settings_files_dir=[]
   hmat_path=[]

   for i in range(len(filepath)):
      temp=filepath[i].get()
      if (os.path.isfile(temp+'/hmat.json')):
         settings_files_dir.append(temp+'/settings_files')
         hmat_path.append(temp+'/hmat.json')
      
   
   print settings_files_dir
   print hmat_path


   for i in range(len(hmat_path)):
      out=os.path.isfile(hmat_path[i]) 
      print out

   #settings_files_dir=['D:/Duke/Sony/cameraData/multizonejsonexport/zone1/settings_files','D:/Duke/Sony/cameraData/multizonejsonexport/zone2/settings_files']

   #hmat_path=['D:/Duke/Sony/cameraData/multizonejsonexport/zone1/hmat.json','D:/Duke/Sony/cameraData/multizonejsonexport/zone2/hmat.json']

   f=open(hmat_path[0])

   h=json.load(f)

   mCamIds=h['mCamId']


   zones=len(settings_files_dir)

   campan=['']*zones
   camtilt=['']*zones
   camzoom=['']*zones
   camfocus=['']*zones
   camwarp=[0]*zones

   zoneZoom=[0]*zones
   zoneX=[0]*zones
   zoneY=[0]*zones

   for i in range(zones):
      campan[i]=['']*len(mCamIds)
      camtilt[i]=['']*len(mCamIds)
      camzoom[i]=['']*len(mCamIds)
      camfocus[i]=['']*len(mCamIds)
      camwarp[i]=[0]*len(mCamIds)
      
      zoneZoom[i]=int(zoneZoomVar[i].get())
      zoneX[i]=int(zoneXVar[i].get())
      zoneY[i]=int(zoneYVar[i].get())
   print 'here it is'
   print zoneZoom
   print zoneX
   print zoneY
   print 'done'



   for i in range(zones):

      f=open(hmat_path[i])

      h=json.load(f)

      mCamIds=h['mCamId']

      print mCamIds
      hmats=h['hmat']

      settings_files=['']*len(mCamIds)
      #campan=[[0],[0]*len(mCamIds)]
   


      print campan
      #camtilt=[[0],[0]*len(mCamIds)]
      #camzoom=[[0],[0]*len(mCamIds)]
      #camfocus=[0]*len(mCamIds)

      for ctr,id in enumerate(mCamIds):
         settings_files[ctr]=settings_files_dir[i]+'/ptzsettings'+str(id)+'.txt'

      print settings_files

      for ctr,current_file in enumerate(settings_files):
         out=sonyptz.read_saved_PTZF_string(current_file)
   
         campan[i][ctr]=out[0]
         camtilt[i][ctr]=out[1]
         camzoom[i][ctr]=out[2]
         camwarp[i][ctr]=hmats[0][ctr]
         print hmats[0][ctr]


      #print campan
      #print camtilt
      #print camzoom
      #print camwarp

   writeMultiZone(mCamIds,campan,camtilt,camzoom,camwarp,zoneZoom,zoneX,zoneY)


def writeMultiZone(mCamIds,mechPan,mechTilt,mechZoom,camWarp,zoneZoom,zoneX,zoneY):

   fieldStringCamId="mcamId"
   fieldStringMechPan="mechPan"
   fieldStringMechTilt="mechTilt"
   fieldStringMechZoom="mechZoom"

   zoneStringZoom="zoneZoom"
   zoneXPosString="zoneXpos"
   zoneYPosString="zoneYpos"

   numCams=len(mCamIds)
   numZones=len(zoneZoom)

   #zoneZoom=[1,2,2]
   #zoneX=[0,-1,1]
   #zoneY=[0,1,-1]

   camId=[0]*numCams

   #mechPan=[]
   #mechTilt=[]
   #mechZoom=[]


   print('mechpan is')
   print mechPan

   print camId
   #allEntries=[]

   testH=(np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]))

   cropBox=[0,0,1080,1920]

   #allEntries.append({"Version":4,"CameraMake":"Sony","CameraModel":"SNC-   WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   allEntries=({"Version":4.2,"CameraMake":"Sony","CameraModel":"SNC-WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   zoneEntries=[]

   for j in range(numZones):

       zoneEntry=dict()
       #mechPan.append([0]*numCams)
       #mechTilt.append([0]*numCams)
       #mechZoom.append([0]*numCams)
       for i in range(numCams):
          camId[i]=i+1
          #mechPan[j][i]=i*10+j
          #mechTilt[j][i]=i*100+j
          #mechZoom[j][i]=i*1000+j
       
       print camId
       print mechPan
       print mechTilt
       print mechZoom

       #camGeomEntries=dict()
       camGeomEntries=[]
       #mechPtzEntries.append({fieldStringCamId:camId[i],fieldStringMechPan:mechPan[j][i],fieldStringMechTilt:mechTilt[j][i],fieldStringMechZoom:mechZoom[j][i],"HwarpRow1":(1,0,0,0),"HwarpRow2":(0,1,0,0),"HwarpRow3":(0,0,1,0),"HwarpRow4":(0,0,0,0)})

       for i in range(numCams):
       
          camGeomEntry=dict() 
          #camGeomEntries.append({fieldStringCamId:camId[i],fieldStringMechPan:mechPan[j][i],fieldStringMechTilt:mechTilt[j][i],fieldStringMechZoom:mechZoom[j][i],"Hwarp":testH,"cropBox":cropBox})
          camGeomEntry[fieldStringCamId]=camId[i]
          camGeomEntry[fieldStringMechPan]=mechPan[j][i]
          camGeomEntry[fieldStringMechTilt]=mechTilt[j][i]
          camGeomEntry[fieldStringMechZoom]=mechZoom[j][i]
          camGeomEntry["Hwarp"]=camWarp[j][i]
          camGeomEntry["cropBox"]=cropBox

       
          #mechPtzEntries[fieldStringCamId]=camId[i]
          #mechPtzEntries[fieldStringMechPan]=mechPan[j][i]
          #mechPtzEntries[fieldStringMechTilt]=mechTilt[j][i]
          #mechPtzEntries[fieldStringMechZoom]=mechZoom[j][i]
          #mechPtzEntries["Hwarp"]=testH
          #mechPtzEntries["cropBox"]=cropBox
       
          #camGeomEntries[str(i+1)]=camGeomEntry
          camGeomEntries.append(camGeomEntry)
       print camGeomEntries
    
       zoneEntry["zoneID"]=j+1
       zoneEntry[zoneStringZoom]=zoneZoom[j]
       zoneEntry[zoneXPosString]=zoneX[j]
       zoneEntry[zoneYPosString]=zoneY[j]
       zoneEntry["camGeometries"]=camGeomEntries
    
    
    
       #zoneEntries[str(j+1)]=zoneEntry
       zoneEntries.append(zoneEntry)
    
       #allEntries.append({'zoneSettings':{str(j):zoneEntry}})

   allEntries['zoneSettings']=zoneEntries
    
   print json.dumps(allEntries,sort_keys=True,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)

   test=np.array([1,2,3])
   print json.dumps((test,test),cls=NumpyAwareJSONEncoder)
   path='D:/Duke/Sony/Documents'
   outputfile=path+'/ringsystem_0001_'+strftime("%Y%m%d%H%M")+'.json'

   with open(outputfile, 'w') as outfile:
      json.dump(allEntries,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)
