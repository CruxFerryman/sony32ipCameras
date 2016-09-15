#ptz fields
import json
import numpy as np
from time import strftime
#path="C:\\Users\\Scott McCain\\Documents\\aqueti\\datasets\\20150322\\AlignmentJPEGS\\"
#path='//home//mosaic//src//cameraSetup//images//'
#path='D:/Duke/Sony/data/20150326/frame_52/'

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def writeOneZone(path):

   fieldStringCamId="mCamId"
   fieldStringMechPan="mechPan"
   fieldStringMechTilt="mechTilt"
   fieldStringMechZoom="mechZoom"

   zoneStringZoom="zoneZoom"
   zoneXPosString="zoneXpos"
   zoneYPosString="zoneYpos"

   numCams=10
   numZones=3

   zoneZoom=[1,2,2]
   zoneX=[0,-1,1]
   zoneY=[0,1,-1]

   camId=[0]*numCams

   mechPan=[]
   mechTilt=[]
   mechZoom=[]


   print('mechpan is')
   print mechPan

   print camId
   #allEntries=[]

   testH=(np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]))

   #cropBox=[171,296,747,1328]
   cropBox=[100,100,980,1820]
   #allEntries.append({"Version":4,"CameraMake":"Sony","CameraModel":"SNC-WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   allEntries=dict()

   allEntries['array_geometry']=({"version":3,"image_width":1920,"image_height":1080,"crop_box":cropBox})

   zoneEntries=[]

   #for j in range(numZones):

   colorH=[[1,0,0],[0,1,0],[0,0,1]]

   #camGeomEntries=dict()
   camGeomEntries=[]
   #mechPtzEntries.append({fieldStringCamId:camId[i],fieldStringMechPan:mechPan[j][i],fieldStringMechTilt:mechTilt[j][i],fieldStringMechZoom:mechZoom[j]      [i],"HwarpRow1":(1,0,0,0),"HwarpRow2":(0,1,0,0),"HwarpRow3":(0,0,1,0),"HwarpRow4":(0,0,0,0)})

   jsonFile=path+'//hmat.json'
   jsonInfo=json.load(open(jsonFile))

   numCams=len(jsonInfo['mCamId'])

   camId=[0]*numCams



   for i in range(numCams):
      #camId[i]=i+1
      #for server side number start at 1
      camId[i]=jsonInfo['mCamId'][i]
      #for file side start number at 0
      #camId[i]=jsonInfo['mCamId'][i]-1

      camGeomEntry=dict() #camGeomEntries.append({fieldStringCamId:camId[i],fieldStringMechPan:mechPan[j][i],fieldStringMechTilt:mechTilt[j][i],fieldStringMechZoom:mechZoom[j][i],"Hwarp":testH,"cropBox":cropBox})
      camGeomEntry[fieldStringCamId]=camId[i]
      #camGeomEntry["PerspectiveMatrix"]=testH
      temp=jsonInfo['hmat'][0]
      #camGeomEntry["PerspectiveMatrix"]=jsonInfo['hmat'][i]
      camGeomEntry["PerspectiveMatrix"]=temp[i]

      camGeomEntry["ColorAdjustMatrix"]=colorH

   
      #mechPtzEntries[fieldStringCamId]=camId[i]
      #mechPtzEntries[fieldStringMechPan]=mechPan[j][i]
      #mechPtzEntries[fieldStringMechTilt]=mechTilt[j][i]
      #mechPtzEntries[fieldStringMechZoom]=mechZoom[j][i]
      #mechPtzEntries["Hwarp"]=testH
      #mechPtzEntries["cropBox"]=cropBox
   
      #camGeomEntries[str(i+1)]=camGeomEntry
      camGeomEntries.append(camGeomEntry)
   print camGeomEntries

   #zoneEntry["zoneID"]=j+1
   #zoneEntry[zoneStringZoom]=zoneZoom[j]
   #zoneEntry[zoneXPosString]=zoneX[j]
   #zoneEntry[zoneYPosString]=zoneY[j]
   #zoneEntry["camGeometries"]=camGeomEntries



   print jsonInfo

   #zoneEntries[str(j+1)]=zoneEntry
   #zoneEntries.append(zoneEntry)
   allEntries["array_geometry"]["camcal"]=camGeomEntries
   #allEntries.append({'zoneSettings':{str(j):zoneEntry}})

   #allEntries['zoneSettings']=zoneEntries
    
   print json.dumps(allEntries,sort_keys=True,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)

   test=np.array([1,2,3])
   print json.dumps((test,test),cls=NumpyAwareJSONEncoder)
   outputfile=path+'/ringsystem_0001_'+strftime("%Y%m%d%H%M")+'.json'
   
   #print('path is '+path+'//test_onezone.json')
   print('json output for pursuit is '+outputfile)
   #with open(path+'//test_onezone.json', 'w') as outfile:
   with open(outputfile, 'w') as outfile:
      json.dump(allEntries,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)


#writeOneZone(path)
