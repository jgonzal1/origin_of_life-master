import base64
from functools import reduce

def dump_to_html():
  import os
  import re
  files = os.listdir("./cropped")
  k=0
  threshold=9999#46
  output = open('cropped_as_b64.html','w+')
  output.writelines('<style>.pabs{position:absolute}</style>\n')
  for file in files:
    end_string_regex = re.search(r"[\._]",file[8:])
    if(end_string_regex is None):
      end_string = len(file)
    else:
      end_string = 8+end_string_regex.start()
    file_number = file[8:end_string]
    if(file_number == ''):
      file_number = 0
    try:
      int(file_number)
    except:
      print("Este fichero no se guardará: " + file)
    if(file.find('cropped')!=-1):
      if(int(file_number)<threshold):
        with open("cropped/" + file, "rb") as image_file:
          encoded_string = base64.b64encode(image_file.read())
          output.writelines(
            '<span>'+
            '<span class="pabs">'+str(file_number)+'</span>'+
            '<img id="'+file[8:]+'" src="data:image/png;base64,'+encoded_string.decode('utf8')+'"/>'+
            '</span>\n')
          k+=1
          if(k>threshold):
            image_file.close()
            output.close()
            break

def compare_images():
  import io
  from PIL import Image
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd
  from untagged import untagged
  from tagged import tagged
  output = open('philogenetic_tree_tagged_b64.html','w+')
  output.writelines('<style>.pabs{position:absolute}</style>\n')
  k=0
  for img1b64 in untagged:
    if(k<166):
      k+=1
      continue
    try:   
      img1 = Image.open(io.BytesIO(base64.b64decode(img1b64))).convert("RGBA") #RGBA
    except:
      continue
    lowest={"id":"","src":"","diff":999,"pos":0}
    l=0
    print("Scanning "+str(k)+". "+str(round(k/12,2))+"%")
    for img2_with_metadata in tagged:
      img2b64 = img2_with_metadata["src"]
      img2 = Image.open(io.BytesIO(base64.b64decode(img2b64))).convert("RGBA") #RGBA
      try:
        substract = np.subtract(img1, img2)
      except:
        continue
      dif = np.fabs(substract)
      reduce_matrix = dif.sum(axis=0)
      df = pd.DataFrame(reduce_matrix).div(10).agg(['sum']).div(10).agg(['sum']).T.div(10).agg(['sum'])
      img2_with_metadata["diff"] = int(df["sum"]["sum"])
      if(img2_with_metadata["diff"] < lowest["diff"]):
        lowest=img2_with_metadata
        lowest["pos"]=l
      l+=1
      if(l%240 == 0):
        print(str(round(l/12)) + "%")
      if(l==len(tagged)):
        tagged.pop(lowest["pos"])
    print("Diff " + str(lowest["diff"]) + " @ " + lowest["id"] + "\n")
    output.writelines(
      '<span>'+
      '<span class="pabs">'+str(lowest["id"])+'</span>'+
      '<img id="'+str(lowest["id"])+'" src="data:image/png;base64,'+img1b64+'"/>'+
      '<img class="comparer" src="data:image/png;base64,'+lowest["src"]+'"/>'+
      '</span>\n'
    )
    k+=1

compare_images()