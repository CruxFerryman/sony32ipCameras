#ptz fields
import json
import numpy as np



class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def writeMultiZoneJson():

   fieldStringCamId="mcamId"
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

   cropBox=[171,296,747,1328]

   #allEntries.append({"Version":4,"CameraMake":"Sony","CameraModel":"SNC-   WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   allEntries=({"Version":4.2,"CameraMake":"Sony","CameraModel":"SNC-WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   zoneEntries=[]

   for j in range(numZones):

       zoneEntry=dict()
       mechPan.append([0]*numCams)
       mechTilt.append([0]*numCams)
       mechZoom.append([0]*numCams)
       for i in range(numCams):
          camId[i]=i+1
          mechPan[j][i]=i*10+j
          mechTilt[j][i]=i*100+j
          mechZoom[j][i]=i*1000+j
       
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
          camGeomEntry["Hwarp"]=testH
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


   with open('test_big_json_file_clean_rev4_2.json', 'w') as outfile:
      json.dump(allEntries,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)
