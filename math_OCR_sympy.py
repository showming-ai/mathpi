#install latex2sympy ↓
#https://github.com/jackatbancast/latex2sympy
#download zip, unzip and move "latex2sympy" folder to venv/Lib/site-packages

#install requests
#pip install requests

#install sympy
#pip install sympy

#install antlr4
#pip install antlr4-python3-runtime
import requests
import json
from sympy import *
from latex2sympy.process_latex import process_sympy

#math pix API
#core technique: https://github.com/blaisewang/img2latex-mathpix
#get start ↓
#https://accounts.mathpix.com/login
#create one API Key
#Use your own "app_id" and app_key
def image_to_Sympy(filename):
  r = requests.post("https://api.mathpix.com/v3/text",
    files={"file": open(filename,"rb")},
    data={
      "options_json": json.dumps({
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
      })
    },
    headers={
        "app_id": "tch3462_goo_tyai_tyc_edu_tw_af02a3_5dd69e",
        "app_key": "8236c3e7376e2992865ce0e572fff59b422e7d05f8781c9e6256d929f384a025"
    }
  )
  data = json.loads(r.text)
  confidence = "confidence:"+str(data['confidence'])
  print(confidence)
  expr = process_sympy(data["latex_styled"])
  """
  x = symbols('x')
  y = symbols('y')
  x_compile = re.compile('x')
  y_compile = re.compile('y')
  p_integrate = re.compile(r'\\int')
  
  if x_compile.search(data["latex_styled"]) != None and y_compile.search(data["latex_styled"]) != None and p_integrate.search(data["latex_styled"]) == None:
    result = solve(expr,[x,y])
  elif x_compile.search(data["latex_styled"]) != None and y_compile.search(data["latex_styled"]) == None and p_integrate.search(data["latex_styled"]) == None:
    result = solve(expr,x)
  elif x_compile.search(data["latex_styled"]) == None and y_compile.search(data["latex_styled"]) != None and p_integrate.search(data["latex_styled"]) == None:
    result = solve(expr,y)
  else:
    result = expr
  """
  print("result:"+str(expr))
  return confidence, expr

if __name__ == '__main__':
  filename = "test_image_10.jpg"
  image_to_Sympy(filename)