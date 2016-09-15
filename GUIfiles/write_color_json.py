#ptz fields
import json
import numpy as np



class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def writeMultiZone():

   fieldStringCamId="mcamId"
   fieldStringMechPan="mechPan"
   fieldStringMechTilt="mechTilt"
   fieldStringMechZoom="mechZoom"

   zoneStringZoom="zoneZoom"
   zoneXPosString="zoneXpos"
   zoneYPosString="zoneYpos"

   numCams=8
   numZones=1

   zoneZoom=[1]
   zoneX=[0]
   zoneY=[0]

   camId=[0]*numCams

   mechPan=[]
   mechTilt=[]
   mechZoom=[]

   colorMs=[]
   print('mechpan is')
   print mechPan

   print camId
   #allEntries=[]

   testH=(np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]))
   colorM=(np.array([1,0,0,0]),np.array([0,1,0,0]),np.array([0,0,1,0]),np.array([0,0,0,1]))

   cropBox=[171,296,747,1328]

   #allEntries.append({"Version":4,"CameraMake":"Sony","CameraModel":"SNC-   WR630","ImageWidthPixels":1920,"ImageHeightPixels":1080})

   allEntries=({"Version":1,"Description":"Color calibration data used for matching camera outputs"})

   zoneEntries=[]

   for j in range(numZones):

       zoneEntry=dict()
       colorMs=[]
       #mechPan.append([0]*numCams)
       #mechTilt.append([0]*numCams)
       #mechZoom.append([0]*numCams)
       for i in range(numCams):
          camId[i]=i+1
          #mechPan[j][i]=i*10+j
          #mechTilt[j][i]=i*100+j
          #mechZoom[j][i]=i*1000+j
          #colorM[0]=colorM[0]+(i-1)*0.01
          #colorM[1]=colorM[1]+(i-1)*0.01
          #colorM[2]=colorM[2]+(i-1)*0.01
          #colorM[3]=colorM[3]+(i-1)*0.01
          #colorMs.append([np.array([1+0.01*i,0.02*i,0.03*i,0.04*i]),np.array([0,1+0.03*i,0,0]),np.array([0,0,1+0.06*i,0]),np.array([0,0,0,0])])
          colorMs.append([np.array([1,0,0,0]),np.array([0,1,0,0]),np.array([0,0,1,0]),np.array([0,0,0,1])])
       
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
          #camGeomEntry[fieldStringMechPan]=mechPan[j][i]
          #camGeomEntry[fieldStringMechTilt]=mechTilt[j][i]
          #camGeomEntry[fieldStringMechZoom]=mechZoom[j][i]
          camGeomEntry["ColorAdjustMatrix"]=colorMs[i]
          #camGeomEntry["cropBox"]=cropBox

       
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
       zoneEntry["camGeometries"]=camGeomEntries
    
    
    
       #zoneEntries[str(j+1)]=zoneEntry
       zoneEntries.append(zoneEntry)
    
       #allEntries.append({'zoneSettings':{str(j):zoneEntry}})

   allEntries['ColorSettings']=camGeomEntries
    
   print json.dumps(allEntries,sort_keys=True,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)

   test=np.array([1,2,3])
   print json.dumps((test,test),cls=NumpyAwareJSONEncoder)


   with open('test_color_8entries.json', 'w') as outfile:
      json.dump(allEntries,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)

writeMultiZone()
