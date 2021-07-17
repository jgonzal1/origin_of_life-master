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
            '<img id="'+file[8:]+'" src="data:image/png;base64,'+
              encoded_string.decode('utf8')+'"/>'+
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
    '''
    number_to_continue_with = 166
    if(k<number_to_continue_with):
      k+=1
      continue
    '''
    try:
      img1 = Image.open(io.BytesIO(base64.b64decode(img1b64))).convert("RGBA")
    except:
      continue
    lowest={"id":"","src":"","diff":999,"pos":0}
    l=0
    print("Scanning "+str(k)+". "+str(round(k/12,2))+"%")
    for img2_with_metadata in tagged:
      img2b64 = img2_with_metadata["src"]
      img2 = Image.open(io.BytesIO(base64.b64decode(img2b64))).convert("RGBA")
      try:
        substract = np.subtract(img1, img2)
      except:
        continue
      dif = np.fabs(substract)
      reduce_matrix = dif.sum(axis=0)
      df = pd.DataFrame(reduce_matrix).div(
        10).agg(['sum']).div(10).agg(['sum']).T.div(10).agg(['sum']
      )
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

def improve_bad_tagged():
  import io
  from PIL import Image
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd
  from tags_to_improve import tags_to_improve
  from tagged import tagged
  output = open('philogenetic_tree_match_trials.html','w+')
  output.writelines('<style>\n  body{width: 90vw;}\n'+
    '  .pair{margin-right: 1em; border: 1px solid #DDD;}\n'+
    '  .pabs{position:absolute}\n'+
    '</style>\n')
  k=0
  for img1b64 in tags_to_improve:
    '''
    number_to_continue_with = 166
    if(k<number_to_continue_with):
      k+=1
      continue
    '''
    try:
      img1 = Image.open(io.BytesIO(base64.b64decode(img1b64[1]))).convert("RGBA")
    except:
      continue
    lowest={"id":"","src":"","diff":999,"pos":0}
    l=0
    print("Scanning "+str(k)+". "+str(round(k/12,2))+"%")
    for img2_with_metadata in tagged:
      img2b64 = img2_with_metadata["src"]
      img2 = Image.open(io.BytesIO(base64.b64decode(img2b64))).convert("RGBA")
      try:
        substract = np.subtract(img1, img2)
      except:
        continue
      dif = np.fabs(substract)
      reduce_matrix = dif.sum(axis=0)
      df = pd.DataFrame(reduce_matrix).div(
        10).agg(['sum']).div(10).agg(['sum']).T.div(10).agg(['sum']
      )
      img2_with_metadata["diff"] = int(df["sum"]["sum"])
      if(img2_with_metadata["diff"] < (img1b64[0]+2)):
        lowest=img2_with_metadata
        lowest["pos"]=l
        print("Diff " + str(lowest["diff"]) + " @ " + lowest["id"] + "\n")
        output.writelines(
          '<span class="pair">'+
          '<span class="pabs">'+str(lowest["diff"]) + " @ " + lowest["id"]+'</span>'+
          '<img id="'+str(lowest["id"])+'" src="data:image/png;base64,'+img1b64[1]+'"/>'+
          '<img class="comparer" src="data:image/png;base64,'+lowest["src"]+'"/>'+
          '</span>\n'
        )
      l+=1
      if(l%240 == 0):
        print(str(round(l/12)) + "%")
      if(l==len(tagged)):
        tagged.pop(lowest["pos"])
    k+=1
    if(k==len(tags_to_improve)):
      output.writelines(
        '<script>\n'
        '  const pair = document.getElementsByClassName("pair");\n'
        '  Array.from({length: pair.length}, (_,x) => {\n'
        '    const pairEl = pair[x];\n'
        '    pairEl.onclick = () => pairEl.style.display = "none";\n'
        '  })\n'
        '</script>\n'
      )

def substitute_b64_with_png():
  import re
  import pandas as pd
  html_i = open('philogenetic_tree_tagged_b64.html','r')
  html_i_lines = html_i.readlines()
  output = open('philogenetic_tree_tagged_png.html','w+')
  for line in html_i_lines:
    pokedex_number_searching = re.search(
      r'<span class="pabs">(.+?).png</span>',line.strip()
    )
    if(pokedex_number_searching):
      pokedex_number = int(re.search(r'(\d+)',pokedex_number_searching[1])[1])
      if(pokedex_number>721):
        pokedex_number = 0
    else:
      pokedex_number = 0
    img_to_append = re.sub(
      r'<img class="comparer" src="data:image/png;base64,.+?"/>',
      '<img src="256px_as_id_pngs/' +
      str(pokedex_number) + '.png"/>', # pkmn_df["name"][]
      line.strip()
    )
    output.writelines(img_to_append+"\n")

def substitute_philogenetic_svg_with_png():
  import re
  import pandas as pd
  from base64_to_png import base64_to_png
  # pkmn_df = pd.read_csv("pokemon_vs_types.csv") # pkmn_df["name"][]
  svg_i = open('phylogenic_tree.svg', 'r', encoding="utf8")
  svg_i_lines = svg_i.readlines()
  output = open('philogenetic_tree_tagged_png.svg','w+')
  k=0
  perc=0
  for line in svg_i_lines:
    base64_searching = re.search(
      r'xlink:href="data:image/png;base64,(.+)"',line
    )
    if(base64_searching):
      if(base64_to_png[base64_searching[1]]):
        pokemon_ref = base64_to_png[base64_searching[1]]
      else:
        pokemon_ref = "0.png"
    else:
      pokemon_ref = "0.png"
    img_to_append = re.sub(
      r'xlink:href="data:image/png;base64,.+"',
        'href="' + pokemon_ref + '"/>',
      line
    )
    if(img_to_append):
      result = img_to_append
    else:
      result = line
    try:
      output.writelines(result)
    except:
      print(result)
    if(k%370 == 0):
      print(str(perc) + " %")
      perc+=1
    k+=1

substitute_philogenetic_svg_with_png()