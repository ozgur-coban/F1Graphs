from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt

API_BASE_URL='https://api.openf1.org/v1/'
#Bahrain Session Key =9472
#Bahrain Meeting Key = 1229
#Saudi Arabia Session Key =9480
#Saudi Arabia Meeting Key =1230
#Australia Session Key =9488
#Australia Meeting Key =1231

def GetTotalLaps():
    
    response=urlopen(API_BASE_URL+'race_control?session_key=9488')
    data = json.loads(response.read().decode('utf-8'))
    df = pd.DataFrame(data)
    
    return(int((df['lap_number'].tail(1)).to_string(index=False)))

def GetDriverNumbers():
    ReturnList=[]
    response=urlopen(API_BASE_URL+"drivers?session_key=9488")
    data = json.loads(response.read().decode('utf-8'))
    df = pd.DataFrame(data)
    
    string=df['driver_number'].to_string(index=False)
    for i in string.split('\n')[0:]:
        ReturnList.append(i.replace(" ",""))
    return(ReturnList)

 

def GetSessionKey():
    response = urlopen('https://api.openf1.org/v1/sessions?year=2024&country_name=Australia')
    data = json.loads(response.read().decode('utf-8'))
    df=pd.DataFrame(data)
    print(data)


def SetDriverColors():
    ListOfDrivers=GetDriverNumbers()
    dictOfColors={}
    
    for i in ListOfDrivers:
        
        if (i=='1' or i=='11'):
            dictOfColors.update({i:'#3671C6'})
            
        if(i=='16' or i=='55' or i=='38'):
            dictOfColors.update({i:'#F91536'})
            
        if(i=='81' or i=='4'):
            dictOfColors.update({i:'#F58020'})   
            
        if(i=='63' or i=='44'):
            dictOfColors.update({i:'#6CD3BF'})
            
        if(i=='14' or i=='18'):
            dictOfColors.update({i:'#358C75'})
            
        if(i=='22' or i=='3'):
            dictOfColors.update({i:'#5E8FAA'})
            
        if(i=='27' or i=='20'):
            dictOfColors.update({i:'#B6BABD'})
            
        if(i=='23' or i=='2'):
            dictOfColors.update({i:'#37BEDD'})
            
        if(i=='31' or i=='10'):
            dictOfColors.update({i:'#2293D1'})
            
        if(i=='24' or i=='77'):
            dictOfColors.update({i:'#C92D4B'})
            
            
        
    
    return dictOfColors

def IntSetDriverColors():
    ListOfDrivers=GetDriverNumbers()
    IntDictOfColors={}
    for i in ListOfDrivers:
        
        if (i=='1' or i=='11'):
            
            IntDictOfColors.update({int(i):'#3671C6'})
        if(i=='16' or i=='55' or i=='38'):
            
            IntDictOfColors.update({int(i):'#F91536'})  
        if(i=='81' or i=='4'):
            
            IntDictOfColors.update({int(i):'#F58020'})   
        if(i=='63' or i=='44'):
            
            IntDictOfColors.update({int(i):'#6CD3BF'})
        if(i=='14' or i=='18'):
            
            IntDictOfColors.update({int(i):'#358C75'})
        if(i=='22' or i=='3'):
            
            IntDictOfColors.update({int(i):'#5E8FAA'})
        if(i=='27' or i=='20'):
            
            IntDictOfColors.update({int(i):'#B6BABD'})
        if(i=='23' or i=='2'):
            
            IntDictOfColors.update({int(i):'#37BEDD'})
        if(i=='31' or i=='10'):
            
            IntDictOfColors.update({int(i):'#2293D1'})
        if(i=='24' or i=='77'):
            
            IntDictOfColors.update({int(i):'#C92D4B'})
            
        
    
    return IntDictOfColors
