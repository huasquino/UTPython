import requests
import json
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sys
from openpyxl.workbook import Workbook


def funcionConsumeURL(data,url,urlogin,usuariologin,passwordlogin):
    
    tiempoinicio = datetime.now()
    salidas=[]
    
    respuesta = {'input': data, 'url': url, 'tiempo': 0,'codigorespuesta':0,'cuerporespuesta':'','excepcion':''}
    
    print(data)

    try:

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        datalogin ='{"usuario": "%s" , "passusuario": "%s" }' % (usuariologin,passwordlogin)
        response = requests.post(urlogin, datalogin, headers=headers)
        json_data = json.loads(response.text)
        token = json_data["token"]
        
        headerst = {'Authorization': token, 'Content-type': 'application/json'}
        responseFun = requests.post(url, data,headers=headerst)
        salidas.append(responseFun.text)
        #json_data = json.loads(response.text)

        print(responseFun.text)
        
        timepotermina = datetime.now()
        difference = (timepotermina - tiempoinicio).total_seconds()
        codigo = responseFun.status_code

        print(codigo)
        
        respuesta['tiempo']=difference
        respuesta['codigorespuesta']=codigo
        #respuesta['cuerporespuesta']=json_data
        
        print(json_data)
    
    except Exception as e:
        respuesta['excepcion']=str(e)
        
    x = np.array(salidas)
    np.savetxt("outputtext.txt", x, fmt="%s")
    
    return respuesta
       
##########################################################################################################

def main():
    nombreArchivoInput=sys.argv[1]
    url=sys.argv[2]
    urllogin=sys.argv[3]
    
    salidas=[]
    datosInput = pd.read_excel(nombreArchivoInput)
    
    for i in datosInput.index:
        jsonRecord=datosInput.loc[i].to_json(orient='columns')
        json_data = json.loads(jsonRecord)
        
        usuariologin = json_data["usuariologin"]
        passwordlogin = json_data["passwordlogin"]
        
        respuesta = funcionConsumeURL(jsonRecord,url,urllogin,usuariologin,passwordlogin)
        salidas.append(respuesta)
    
    df = pd.DataFrame(salidas)
    df.to_excel(excel_writer = "output.xlsx")
    

if __name__ == '__main__':
    main()