import json
import write_json_multi_zone
import sony_ptz_library as sonyptz

settings_files_dir=['D:/Duke/Sony/cameraData/multizonejsonexport/zone1/settings_files','D:/Duke/Sony/cameraData/multizonejsonexport/zone2/settings_files']

hmat_path=['D:/Duke/Sony/cameraData/multizonejsonexport/zone1/hmat.json','D:/Duke/Sony/cameraData/multizonejsonexport/zone2/hmat.json']

f=open(hmat_path[0])

h=json.load(f)

mCamIds=h['mCamId']


zones=len(settings_files_dir)

campan=['']*zones
camtilt=['']*zones
camzoom=['']*zones
camfocus=['']*zones
camwarp=[0]*zones


for i in range(zones):
   campan[i]=['']*len(mCamIds)
   camtilt[i]=['']*len(mCamIds)
   camzoom[i]=['']*len(mCamIds)
   camfocus[i]=['']*len(mCamIds)
   camwarp[i]=[0]*len(mCamIds)

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

write_json_multi_zone.writeMultiZone(mCamIds,campan,camtilt,camzoom,camwarp)
