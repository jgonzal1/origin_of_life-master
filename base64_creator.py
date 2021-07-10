import os
import base64
files = os.listdir("./cropped")
k=0
output = open('b64.html','w+')
for file in files:
  if(file.find('cropped')!=-1):
    with open(file, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read())
      output.writelines('<p>'+file[8:]+': <img id="'+file[8:]+'" src="data:image/png;base64,'+encoded_string.decode('utf8')+'"/></p>\n')
      k+=1
      if(k>5):
        image_file.close()
        output.close()
        break