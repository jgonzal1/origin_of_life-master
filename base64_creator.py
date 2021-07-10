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
            '  <span class="pabs">'+str(file_number)+'</span>'+
            '  <img id="'+file[8:]+'" src="data:image/png;base64,'+encoded_string.decode('utf8')+'"/>'+
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
  img1b64="iVBORw0KGgoAAAANSUhEUgAAACgAAAAeCAYAAABe3VzdAAAABHNCSVQICAgIfAhkiAAAAdZJREFU WIXtlrFLG1Ecxz8pNYVSyGHpIkIGyUFG4QcScOnUuGUokW75H4p0cnKS1P+hk6J0KC61k0tLKRxk DDSIPAcXqVxACp7Dc7i8Mxcp9N57iMN9lru8exwffr/f912gpKSkpORRU/H5MhHRAFEUVWbXZtf/ l6c+pKIoqoiITjo1ql/GObH2QXC3uZvuLfJ+pwqKiH7x/hVXOxcknRoAjUGAUor2QcD3X3MAXO1c AA9cQRHRqQTU63VGxDQGAc3+mCap3OrKDUfd2ErMWXCaZn8MGwF/3v4FyOQglQes5/CJq9zlSZL7 fbirM7nhRo3RckzSqWUjUBQvM3h5ktAYBIyWY+aXqgC8/Pz83n6lFFCsil5aPIuRa/bHWVAA2iuT RBdIs/M5OF3F+aVqdjWYdgMcdWOgWAWdW/xmfTu39mPxY1ZB01KDTZqtBY3c5t4aW+++3nv+bf+D 0/FisEqxiOiw1QPIyW3urWX3YauX+8zZ4nTMnJ4NgbRacCdr1n1gneLr82OeLbzm9GxI2Op5lZrG SnAyWzpc+Pee6/NjS6U8zimGdN4MRkwp5SUkTik2Yr9/fgKy7643OXCYQdPmqXsAHbZ6TFpf+L/f gyAi2sfxUuKLW+XNyvwgIul9AAAAAElFTkSuQmCC "
  img2b64Oddish="iVBORw0KGgoAAAANSUhEUgAAACgAAAAeBAMAAACs80HuAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAB5QTFRFAAAAMTExSntCnM5KY5xKUlJSe5S95kopWnOU////nwxNQQAAAAF0Uk5TAEDm2GYAAAABYktHRAnx2aXsAAAACW9GRnMAAAEYAAAAWgDTjIhSAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAHgAAALXgCNjDIEAAAAj0lEQVQoz92QOw7CMBBE7RusCaC0JOEAkcMBgu0DGGKJlmbDCejToD02rmcrWqZ8evvRGPMXsWQcAaMdOT+CN3d5msFs0tkHnG7CMvnsAPZLf+lOsPN6i6VkQpjuMcD5/TBEP4LJnDI+f3wz40f2wytvCOXJLwUfIoLQtBVmVVwrhZS5HZRYK7aizBpnfs8XFeMZH59OIdQAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTYtMTItMjdUMjI6MDY6MjctMDU6MDDat3s3AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDE2LTEyLTI3VDIxOjE0OjQwLTA1OjAw0JOXsQAAAABJRU5ErkJggg== "
  img2b64Charizard="iVBORw0KGgoAAAANSUhEUgAAACgAAAAeBAMAAACs80HuAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAACpQTFRFAAAAMTEx/1o695Qp/+YptUI6UlJS1mNCMWtaSoRz////99Zz1rVjvb29CHeo4wAAAAF0Uk5TAEDm2GYAAAABYktHRApo0PRWAAAACW9GRnMAAADwAAAAAADPuK/XAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAHgAAALXgCNjDIEAAABBElEQVQoz5XRMW7CMBQGYL8b2FiVq0odSnsB60GyV1wgg9k6ICuxQCyWJb+pM6zduAE3YMnepZeqEU4AEanF45f3/89JGPv7AB/A0X8Rxi8D+Dq+HYW3QXw/59NjwY/XkbMeQTMwldScjWb6AmVt5qg5TPpO6SEIY2xSeUaeZh+Mdaid79K4kKl1XmwJL7DEBQdbbDdUUM5LRCQv0S13G3I9hj1RQIzLHXV5NdX7hoJFF79U9LmSHqlW7cGmQsiYKstYQdse0m7VZJyiryv4aZvCRcrbIXj+/KHWKV6S664kOAOhaIUW++X5DSiuEorrjyzEdyiv5k5MdIvs6XPoDwt25/kFpiRCcSVaIo0AAAAldEVYdGRhdGU6Y3JlYXRlADIwMTYtMTItMjdUMjI6MDY6MjctMDU6MDDat3s3AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDE2LTEyLTI3VDIxOjE0OjQwLTA1OjAw0JOXsQAAAABJRU5ErkJggg=="
  img2b64=img2b64Oddish
  img1 = Image.open(io.BytesIO(base64.b64decode(img1b64))).convert("RGBA") #RGBA
  img2 = Image.open(io.BytesIO(base64.b64decode(img2b64))).convert("RGBA") #RGBA
  print(img1)
  print(img2)
  dif = np.fabs(np.subtract(img1, img2))
  reduce_matrix = dif.sum(axis=0)
  df = pd.DataFrame(reduce_matrix).div(10).agg(['sum']).div(10).agg(['sum']).T.div(10).agg(['sum'])
  print(df)
  #reduce_rows = reduce_matrix.sum(axis=0)
  #reduce_rows[reduce_rows == np.inf]
  #df = pd.DataFrame(reduce_rows)
  #pd.set_option('mode.use_inf_as_na', True)
  #df.dropna(inplace=True)
  #print(df)
  #imgplot = plt.imshow(dif)
  #imgplot.set_cmap('jet')
  #plt.axis('off')
  #plt.show()

dump_to_html()