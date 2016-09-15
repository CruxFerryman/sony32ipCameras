import json

import numpy as np

class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

fname='zone.json'

newfname='zone_cropped.json'

newCropBox=[0,0,985,1920]



with open(fname) as data_file:
   data=json.load(data_file)

print data["zoneSettings"][0]

print len(data["zoneSettings"])

for zone in data["zoneSettings"]:
   #print zone["camGeometries"]
   #print len(zone["camGeometries"])
   for cam in zone["camGeometries"]:
      print cam["cropBox"]
      cam["cropBox"]=newCropBox

print data

with open(newfname,'w') as outfile:
   json.dump(data, outfile)

#print data

with open(newfname, 'w') as outfile:
   json.dump(data,outfile,indent=4,separators=(',',': '),cls=NumpyAwareJSONEncoder)
