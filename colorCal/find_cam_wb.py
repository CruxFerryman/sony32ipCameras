import cv2
import Image
import numpy as np
import glob
import re
import json
from time import strftime

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

#%    0.9005    0.0735   -0.0899
#%     0.0194    1.0663    0.0421
#%     0.0011   -0.0760    1.03361

A=np.array([np.array([0.9005, 0.0735, -0.0899]),np.array([0.0194,1.0663,0.0421]),np.array([0.0011,-0.760,1.03361])])

A=np.array([np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])])



def srgb2linear(imin):
#   out=np.pow(imin,2.2)
   out=np.power((imin)/256,1)
   return out

def linear2srgb(imin):
   out=256*np.power(imin,1/1)
   return out

def findMean(fname):

   rows=400
   rowe=700
   cols=750
   cole=1250
   temp=cv2.imread(fname)
   i=Image.open(fname)
   a=np.asarray(i,np.float)
   b=srgb2linear(a)
   r=b[rows:rowe,cols:cole,0]
   g=b[rows:rowe,cols:cole,1]
   b=b[rows:rowe,cols:cole,2]
   print r.shape
   return(np.mean(r),np.mean(g),np.mean(b))

def checkImage(fname,mcamId,gain,offset):
   i=Image.open(fname)
   a=np.asarray(i,np.float)
   b=srgb2linear(a)
   for i in range(len(gain)):
      #b[:,:,i]=(b[:,:,i]-offset[i])/gain[i]
      b[:,:,i]=b[:,:,i]*gain[i]+offset[i]

      print gain[i]
      print offset[i]
      
   

   c=linear2srgb(b)
   #print a.astype(np.uint8)
   #c=b*256
   img=Image.fromarray(c.astype(np.uint8),'RGB')
   img.save('test/'+str(mcamId)+'.jpg')
   print 'find mean gets '
   print findMean('test/'+str(mcamId)+'.jpg')

def getImageFilenames(imagePath):
   #mcamIds=[]
   #imageFilenames=[]
   mcamIds=[]
   #del imageFilenames[:]
   imageFilenames=[]   
   glob_out=glob.glob(imagePath+'/mcam*.jpg')
   print ('path is '+imagePath)
   numfiles=len(glob_out)
   print('Found '+str(numfiles)+' jpegs in directory')
   #numfiles_status.set(str(numfiles)+' jpegs found')
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
   return (mcamIds,imageFilenames)

def getGainOffset(ref1,ref2,cam1,cam2):

   
   print ref1
   print cam1


   gain=(cam1-cam2)/(ref1-ref2)
   offset=cam1-ref1*gain

   offset=-offset/gain

   gain=1/gain

   return (gain,offset)

def makeColorMats(mcamIds,A,gains,offsets):
   cMats=[]
  
   for i in range(len(mcamIds)):
      print gains[i]
      temp=np.zeros([4,4])
      temp[0:3,0:3]=np.dot(A,np.diag(gains[i]))
      temp[3,3]=1
      temp[0:3,3]=np.array(offsets[i])
      #cMats.append(np.array(temp))

      cMats.append([np.array(temp[0,0:4]),np.array(temp[1,0:4]),np.array(temp[2,0:4]),np.array(temp[3,0:4])]) 


   print cMats
   return (cMats)

def writeColorJson(camId,colorMs):

   fieldStringCamId="mcamId"
   camGeomEntries=[]
   for i in range(len(camId)):
       
      camGeomEntry=dict() 
      camGeomEntry[fieldStringCamId]=camId[i]
      camGeomEntry["ColorAdjustMatrix"]=colorMs[i]
      camGeomEntries.append(camGeomEntry)
                

   print camGeomEntries
   return camGeomEntries

#caldir='D:/Duke/Sony/cameraData/20150430/082953ColorCal/f*'

caldir='D:/Duke/Sony/cameraData/20150504/114142ColorCal/'

glob_out=glob.glob(caldir+'f*')
print glob_out





fnums=[]

for cdir in glob_out:
   #print cdir
   fnums.append(cdir[len(caldir)-1:])

print fnums   

(imagefiles,mcamIds)=getImageFilenames(glob_out[0])

print imagefiles
print mcamIds

#imagefiles=glob.glob(glob_out[0]+'/mcam_*.jpg')

numfiles=len(imagefiles)
print numfiles

numfstops=len(glob_out)
print numfstops

avgcolor=np.zeros((3,numfstops,numfiles))

for fnumctr,cdir in enumerate(glob_out):
   (mcamIds,imagefiles)=getImageFilenames(cdir)
   print 'right here11'
   print imagefiles[0]
   for mcamctr,cfile in enumerate(imagefiles):
      #(temp,temp2,temp3)=findMean(cfile)
      #avgcolor[0,fnumctr,mcamctr]=temp
      (avgcolor[0,fnumctr,mcamctr],avgcolor[1,fnumctr,mcamctr],avgcolor[2,fnumctr,mcamctr])=findMean(cfile)
      #,avgcolor(2,fnumctr,mcamtr),avgcolor(3,fnumctr,mcamtr))=findMean(cfile)
      
      #print temp
   #if fnumctr==0:
   #   break
   #break

refcolor=avgcolor[:,:,0]
print 'refcolor is'
print refcolor


cmats=[]

for mcamctr,cfile in enumerate(imagefiles):
   bigh=np.zeros((4,4))

   meascolor=avgcolor[:,:,mcamctr]
   rpoly=np.polyfit(refcolor[0,:],meascolor[0,:],1)
   print rpoly

   bigh[0,0]=1/rpoly[0]
   bigh[0,3]=-rpoly[1]/rpoly[0]

   gpoly=np.polyfit(refcolor[1,:],meascolor[1,:],1)
   print gpoly

   bigh[1,1]=1/gpoly[0]
   bigh[1,3]=-gpoly[1]/gpoly[0]

   bpoly=np.polyfit(refcolor[2,:],meascolor[2,:],1)
   print bpoly

   bigh[2,2]=1/bpoly[0]
   bigh[2,3]=-bpoly[1]/bpoly[0]
   bigh[3,3]=1
   
   #cmats.append(bigh)

   cmats.append([np.array(bigh[0,0:4]),np.array(bigh[1,0:4]),np.array(bigh[2,0:4]),np.array(bigh[3,0:4])]) 

print cmats

   
print bigh
  # for mcam_ctr,cfile in enumerate(imagefiles):



print avgcolor
bright_cal_dir='D:/Duke/Sony/caldata/more_color_data/094644_sheet_gain5'

bright_cal_dir='D:/Duke/Sony/caldata/140139_sheet_3'

dim_cal_dir='D:/Duke/Sony/caldata/more_color_data/094609_sheet_gain1'

dim_cal_dir='D:/Duke/Sony/caldata/140044_sheet_1'
#(mcamIds,imageFilenames)=getImageFilenames(bright_cal_dir)






#print mcamIds
#print imageFilenames

#fname=bright_cal_dir+'/mcam_1.jpg'

#temp=cv2.imread(fname)

#cv2.imshow('test',temp)
#cmeans=[]
#dimmeans=[]
#camGains=[]
#camOffsets=[]
#for fname in imageFilenames:
#   cmeans.append(findMean(fname))

#(mcamIds,dimFilenames)=getImageFilenames(dim_cal_dir)
#for fname in dimFilenames:
#   dimmeans.append(findMean(fname))

#print 'alpha'
#(g,o)=getGainOffset(cmeans[0][0],dimmeans[0][0],cmeans[1][0],dimmeans[1][0])

#for i in range(len(mcamIds)):
#   (r,ro)=getGainOffset(cmeans[0][0],dimmeans[0][0],cmeans[i][0],dimmeans[i][0])
   
#   (g,go)=getGainOffset(cmeans[0][0],dimmeans[0][0],cmeans[i][1],dimmeans[i][1])
#   (b,bo)=getGainOffset(cmeans[0][0],dimmeans[0][0],cmeans[i][2],dimmeans[i][2])
#   camGains.append([r,g,b])
#   camOffsets.append([ro,go,bo])

#print 'gain is'
#print g
#print 'offset is'


#print(camGains)
#print(camOffsets)


#for i in range(len(mcamIds)):
#   checkImage(imageFilenames[i],mcamIds[i],camGains[i],camOffsets[i])

   #checkImage(dimFilenames[i],mcamIds[i],camGains[i],camOffsets[i])

#cMats=makeColorMats(mcamIds,A,camGains,camOffsets)

camColorEntries=writeColorJson(mcamIds,cmats)

#   checkImage(dimFilenames[i],mcamIds[i],camGains[i],camOffsets[i])

#checkImage(imageFilenames[0],mcamIds)
allEntries=({"Version":1,"Description":"Color calibration data used for matching camera outputs"})
allEntries['ColorSettings']=camColorEntries


foldername=strftime("%Y%m%d/%H%M%S")

writefname='color_'+strftime("%Y%m%d%H%M")+'.json'

with open(caldir+writefname, 'w') as outfile:
   json.dump(allEntries,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)



