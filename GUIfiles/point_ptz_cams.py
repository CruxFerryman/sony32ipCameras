import sony_ptz_library as sonyptz
import cv2
import Tkinter


settings_fname='ptz0settings.txt'
 
degrees_per_hex_val=0.022059
max_pan_degrees=180
min_pan_degrees=-180
min_tilt_degrees=-155
max_tilt_degrees=65


zoom_ifov_multiplier=0.03598
zoom_fit_p1=-4.5545e-5
zoom_fit_p0=1.0131


   
ip='10.1.201.222'
filename='images/temp.jpg'

sonyptz.grabCamImage(ip,filename)
   

img=cv2.imread(filename)
(height,width) = img.shape[:2]
print('image width is '+str(width)+' image height is '+str(height))

imagecenterx=width/2
imagecentery=height/2


(cenx,ceny)=sonyptz.findCentroid(img,HueLowLimit,HueHighLimit)

print('centroid x is ' +str(cenx)+' centroid y is '+str(ceny))

#Get current camera's PTZF 
sonyptz.get_PTZF()

panstep=100*camzoom[0]
tiltstep=100*camzoom[0]



(newpan,newtilt)=sonyptz.findPTZFdir(panstep,tiltstep,imagecenterx,imagecentery,cenx,ceny)
#changePTZFCallBack(newpan,newtilt,camzoom[0],camfocus[0])



print('New pan is '+str(newpan)+' new tilt is '+str(newtilt))

sonyptz.centerCam(panstep,tiltstep)
##
panstep=50*camzoom[0]
tiltstep=50*camzoom[0]
##

#cv2.waitKey(0)
sonyptz.centerCam(panstep,tiltstep)
#cv2.waitKey(0)

sonyptz.centerCam(panstep,tiltstep)
#cv2.waitKey(0)

sonyptz.centerCam(panstep,tiltstep)


##
panstep=10*camzoom[0]
tiltstep=10*camzoom[0]
##







cv2.destroyAllWindows()
