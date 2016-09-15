import cv2
import numpy as np
import time
import json

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def findCentroid(img,numCentroids,HueLowLimit,HueHighLimit,SatLowLimit,ballSearchSize):


   #cv2.line(img,(0,0),(511,511),(255,0,0),50)


   #
   print('Low Hue Limit is ')
   print(HueLowLimit.get())
   
   img=cv2.GaussianBlur(img,(5,5),0)

   #mask=img.copy()
   mask=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

   mask[:,:]=0
 
   mask=np.zeros(img.shape, dtype=np.uint8)
   

   (c,r,wl)=mask.shape
   r=r/2
   c=c/2

   srch_rad=int(0.5*0.01*ballSearchSize.get()*(np.sqrt(mask.shape[0]*mask.shape[0]+mask.shape[1]*mask.shape[1])))


   cv2.circle(mask,(r,c),srch_rad,(255,255,255),-1)

   img=img & mask

   #res=cv2.bitwise_and(img,img,mask= mask)

   #cv2.imshow("Masked original", img)

   hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   #green tape from lab
   #lower_green=np.array([60, 128, 128])
   #upper_green=np.array([80, 255, 255])
   #note opencv hue values go from 0 to 180
   #lower_green=np.array([70, 100, 20])
   #upper_green=np.array([83, 255, 255])
   #lower_green=np.array([40, 50, 20])
   #upper_green=np.array([100, 255, 255])
   lower_green=np.array([HueLowLimit.get(), SatLowLimit.get(), 20])
   
   upper_green=np.array([HueHighLimit.get(), 255, 255])

   mask=cv2.inRange(hsv,lower_green,upper_green)
   
   #circle_mask=mask.copy()
   #circle_mask[:,:]=0

   

   #srch_rad=int(0.5*0.01*ballSearchSize.get()*(np.sqrt(mask.shape[0]*mask.shape[0]+mask.shape[1]*mask.shape[1])))


   #print 'search radius is' + str(srch_rad)


   #(c,r)=mask.shape
   #r=r/2
   #c=c/2

   #cv2.circle(circle_mask,(r,c),srch_rad,255,-1)

   

   centroid_vals=[0]*numCentroids
   
   res=cv2.bitwise_and(img,img,mask= mask)
   
   #res2=cv2.bitwise_and(img,img,mask= mask)
   
   #res2=cv2.bitwise_and(mask,mask,mask= circle_mask)
   
   #res=cv2.bitwise_and(circle_mask,circle_mask,mask= mask)
  
   (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   print "I found %d black shapes" % (len(cnts))
   blobArea=[0]*len(cnts)

   
   r = 500.0 / mask.shape[1]
   dim = (500, int(mask.shape[0] * r))
   resizedmask = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA)




   cv2.imshow("Mask", resizedmask)
   
   if len(cnts)==0:
      print('ERROR: Did not find any objects in the image')
      for centroidCtr in range(numCentroids):
         centroid_vals[centroidCtr]={'x':0,'y':0}
      return centroid_vals
   if len(cnts)>500:
      print('ERROR: Found too many objects, your color range is too large')
      for centroidCtr in range(numCentroids):
         centroid_vals[centroidCtr]={'x':0,'y':0}
      return centroid_vals


   for ctr,c in enumerate(cnts):
         # draw the contour and show it
         #cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
         #cv2.waitKey(33)
         #M=cv2.moments(c)
         #print M
         #print('Contour area is '+str(cv2.contourArea(c)))
         blobArea[ctr]=cv2.contourArea(c)
         print('Blob area is '+ str(blobArea[ctr]))  
   for centroidCtr in range(numCentroids):
      # loop over the contours
      

      maxindex=np.argmax(blobArea)
      bigC=cnts[maxindex]
      #M=cv2.moments(bigC)

      #cx=int(M['m10']/M['m00'])
      #cy=int(M['m01']/M['m00'])

      #print M

      #print('centroid x is '+str(cx)+' centroid y is '+str(cy))
   
      (x,y),radius=cv2.minEnclosingCircle(bigC)
      center=(int(x),int(y))
      radius=int(radius)
      cv2.circle(img,center,radius, (0, 0, 255),2)
      print('center x is '+str(x)+' center y is '+str(y)+' radius is '+str(radius))           
      #centroid_vals[centroidCtr]=(x,y)
      centroid_vals[centroidCtr]={'x': x,'y': y}
      
      
      blobArea[maxindex]=0

   r = 1000.0 / img.shape[1]
   dim = (1000, int(img.shape[0] * r))
   resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

   #cv2.imshow('image',img)
   #cv2.putText(resized,"HELLO",(5,25),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255))
   #cv2.waitKey(0)
   cv2.imshow("resized", resized)
   cv2.waitKey(33)
   return centroid_vals
   
def MakeWarpTransforms(alignmentPoints):
   
   
   #x_points=np.array
   numImages=len(alignmentPoints)
   numAlignmentPoints=len(alignmentPoints[0])
   print('length of alignment points is '+str(numImages))
   print('number of entries ' +str(numAlignmentPoints))
   
   x_points=np.zeros((numImages,numAlignmentPoints))
   y_points=np.zeros((numImages,numAlignmentPoints))
   
   tempx=np.zeros(numAlignmentPoints)
   tempy=np.zeros(numAlignmentPoints)
   
   Hmat=[]
   
   for ctr1,s in enumerate(alignmentPoints):
      print('here they come')
      for ctr2,ss in enumerate(s):
         #print ss
         #print('x is '+str(ss['x'])+' and y is '+str(ss['y']))
         #x_points[ctr1,ctr2]=ss['x']
         #y_points[ctr1,ctr2]=ss['y']
         tempx[ctr2]=ss['x']
         tempy[ctr2]=ss['y']
         #print x_points
         #print y_points
      #x_points[
      ind=tempy.argsort()
      tempx=tempx[ind]
      tempy=tempy[ind]
      #print('sorted y is '+str(tempy)+' sorted x is '+str(tempx))
      x_points[ctr1,:]=tempx
      y_points[ctr1,:]=tempy
   print('X alignment points')
   print x_points
   print('Y alignment points')
   print y_points
   
   u=x_points[0,:]
   v=y_points[0,:]
   print('reference x')
   print u
   print('reference y')
   print v
   u_bar=u.mean()
   v_bar=v.mean()
   u_tilde=u-u_bar
   v_tilde=v-v_bar
   A=(u_tilde*u_tilde+v_tilde*v_tilde).sum()
   for ctr1,s in enumerate(alignmentPoints):
      if (ctr1==0):
         theta=0
         mag=1
         xoffset=0
         yoffset=0
      else:
         x=x_points[ctr1,:]
         y=y_points[ctr1,:]
      
         x_bar=x.mean()
         y_bar=y.mean()
      
         x_tilde=x-x_bar
         y_tilde=y-y_bar
      
         B=(x_tilde*x_tilde+y_tilde*y_tilde).sum()
         C=(u_tilde*x_tilde+v_tilde*y_tilde).sum()
         D=(u_tilde*y_tilde-v_tilde*x_tilde).sum()
      
         print('A is '+str(A)+' B is '+str(B)+' C is '+str(C)+' D is '+str(D))
      
         theta=np.arctan2(D,C)
         mag=(C/B)*np.cos(theta)+(D/B)*np.sin(theta)
         xoffset=u_bar-mag*(x_bar*np.cos(theta)+y_bar*np.sin(theta))
         yoffset=v_bar-mag*(-x_bar*np.sin(theta)+y_bar*np.cos(theta))
      
      Hmat.append([[mag*np.cos(theta),-mag*np.sin(theta),0],[mag*np.sin(theta),mag*np.cos(theta),0],[xoffset,yoffset,1]])
   return Hmat
   
def checkHmatAlignment(img,Hmat):
   rows,cols,ch=img.shape
   warpMat=np.array(Hmat)
   warpMat=warpMat[0:3,0:2]
   print('warp mat is')
   print warpMat
   print('done')
   out=cv2.warpAffine(img,warpMat.transpose(),(cols,rows))
   
   return out

def writeWarpMat(path,mcamIds,Hmat):
   #Below dumps the warp transform data H into a json file   
   out=dict()
   out['hmat']=Hmat
   out['mCamId']=mcamIds   
   print('in here')
   print(path+'//hmat.json')

   with open(path+'//hmat.json', 'w') as outfile:
      json.dump(out,outfile,indent=4,separators=(',',': '))
   #End dump warp transform into json file





