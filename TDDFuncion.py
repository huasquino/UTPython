import requests
import json
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sys
from openpyxl.workbook import Workbook


def funcionConsumeURL(data,url):
    
    tiempoinicio = datetime.now()
    salidas=[]
    
    respuesta = {'input': data, 'url': url, 'tiempo': 0,'codigorespuesta':0,'cuerporespuesta':'','excepcion':''}
    
    print(data)

    try:
        
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data,headers=headers)
        salidas.append(response.text)
        #json_data = json.loads(response.text)
        
        timepotermina = datetime.now()
        difference = (timepotermina - tiempoinicio).total_seconds()
        codigo = response.status_code
        
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
    
    salidas=[]
    datosInput = pd.read_excel(nombreArchivoInput)
    
    for i in datosInput.index:
        jsonRecord=datosInput.loc[i].to_json(orient='columns')
        respuesta = funcionConsumeURL(jsonRecord,url)
        salidas.append(respuesta)
    
    df = pd.DataFrame(salidas)
    df.to_excel(excel_writer = "output.xlsx")
    

if __name__ == '__main__':
    main()