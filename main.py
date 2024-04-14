from urllib.request import urlopen
import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so
import numpy as np
import time
import os
import statsmodels.api as sm
from data import *

my_path = os.path.dirname(os.path.abspath(__file__))+'\images'
API_BASE_URL='https://api.openf1.org/v1/'
SessionLaps=GetTotalLaps()
DriverNumbers=GetDriverNumbers()
#Bahrain Session Key =9472
#Bahrain Meeting Key = 1229
#Saudi Arabia Session Key =9480
#Saudi Arabia Meeting Key =1230
#Australia Session Key =9488
#Australia Meeting Key =1231










##################################################
def GetTopSpeed3():
    dict={}
    for drivernumber in DriverNumbers:
        
        
        response=urlopen(API_BASE_URL+'laps?session_key=9488&driver_number='+drivernumber)
        data = json.loads(response.read().decode('utf-8'))
        df = pd.DataFrame(data)
        try:
            SortedDF=df.sort_values(by="st_speed" , ascending=False)
        except:
            Exception
        maxSpeed=SortedDF['st_speed'].iloc[0]
        dict.update({drivernumber:maxSpeed})
        
    return dict

def GraphTopSpeed():
    time.sleep(5)

    dictTopSpeed=GetTopSpeed3()

    df = pd.DataFrame([[key,value] for key,value in dictTopSpeed.items()],columns=["DriverNumber","TopSpeed"])

    ax=sns.barplot(x='DriverNumber',y='TopSpeed',data=df,palette=SetDriverColors())
    for container in ax.containers:

        ax.bar_label(container)

    my_file1 = 'AustraliaTopSpeed.png'

    plt.savefig(os.path.join(my_path, my_file1),dpi=300)  







##################################################################
######################################################
def GetStints3():
    
    CombinedDic={'0':{'SOFT1':0,'MEDIUM1':0,'HARD1':0,'SOFT2':0,'MEDIUM2':0,'HARD2':0,'SOFT3':0,'MEDIUM3':0,'HARD3':0,'SOFT4':0,'MEDIUM4':0,'HARD4':0}}
    for drivernumber in DriverNumbers:
        response=urlopen(API_BASE_URL+'stints?session_key=9488&driver_number='+drivernumber)
        data = json.loads(response.read().decode('utf-8'))
        df=pd.DataFrame(data)
        Lap_start=df['lap_start'].to_string(index=False, header=False).split('\n')
        Lap_end=df['lap_end'].to_string(index=False, header=False).split('\n')
        StintNumber=df['stint_number'].to_string(index=False, header=False).split('\n')
        CompoundList=df['compound'].to_string(index=False, header=False).split('\n')
        
        Stint_lengths=[]
        for i,j in zip(Lap_start,Lap_end) :
            Stint_lengths.append(int(int(j)-int(i)))
        tempdic={}
        
        l=0
        for k,z in zip(CompoundList,StintNumber):
            
            k=k.replace(' ','')
            k=k+z
            
            
            while l<len(Stint_lengths) :
                
                tempdic.update({k:Stint_lengths[l]})
                
                break
                
            l=l+1
            
        
        CombinedDic.update({drivernumber:tempdic})
        
        
        
    return CombinedDic

def GraphGetStints():
    time.sleep(5)
    dictStints=GetStints3()



    df = pd.DataFrame.from_dict(dictStints, orient='index')

    df.insert(0,'DriverNumbers',df.index.values,True)


        
    ax=df.set_index('DriverNumbers').plot(kind='bar', stacked=True,  color=['#f26161', '#ffe200','#dddddd','#f03939','#dbc300','#cbcbcb','#ea0909','#bda800','#a6a6a6','#9a0707','#938200','#818181'],legend=False)

    for c in ax.containers:

        
        labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in c]
        
        
        ax.bar_label(c,fontsize=6, labels=labels, label_type='center')
        

    my_file2 = 'AustraliaStints.png'


    plt.savefig(os.path.join(my_path, my_file2),dpi=300)  

####################

def GetPositionChanges():
    bigDicDates={}
    bigDicPositions={}
    for drivernumber in DriverNumbers:
        response=urlopen(API_BASE_URL+'position?session_key=9488&driver_number='+drivernumber)
        data = json.loads(response.read().decode('utf-8'))
        df = pd.DataFrame(data)
        
        dates=df['date'].to_string(index=False, header=False).replace('\n',' ')
        positions=df['position'].to_string(index=False, header=False).replace('\n',' ')
        
        dictDates={drivernumber:dates}
        dictPositions={drivernumber:positions}

        bigDicDates.update(dictDates)
        bigDicPositions.update(dictPositions)
    

    
    return bigDicDates , bigDicPositions
    

#dict1 , dict2 = GetPositionChanges()
#print(dict1)
#print(dict2)

############################################################################################













#########################################################################################################################
def getIntervalToLeader(): 
    mainDF=pd.DataFrame()
    
    for drivernumber in DriverNumbers:
        response=urlopen('https://api.openf1.org/v1/intervals?session_key=9472&driver_number='+drivernumber)
        data=json.loads(response.read().decode('utf-8'))
        df=pd.DataFrame(data)
        df=df[['gap_to_leader','driver_number']]
        df=df.replace(to_replace=['1L','1 L' ,'2L','2 L','3L','3 L','4L','4 L','5L','5 L' ,'45L','45 L','49L','49 L'],value=200)
        
        
        mainDF=pd.concat([mainDF,df])
        mainDF=mainDF.reset_index(drop=True)
    
    
    mainDF.insert(0,'Total_Laps',np.arange(mainDF.shape[0]),True)
    
    return mainDF

def GraphGetIntervalToLeader():
    time.sleep(5)
    itlData=getIntervalToLeader()


    gfg=sns.lineplot(y='Total_Laps',x='gap_to_leader',hue='driver_number',data=itlData,legend='full',palette=IntSetDriverColors())

    my_file3 = 'AustraliaIntervalToLeader.png'
    plt.savefig(os.path.join(my_path, my_file3),dpi=300) 
    


####################################################################################################################################

def getStintToCompare():
    driversToCompare=['4','11','55','63']
    mainDF=pd.DataFrame()
    for drivernumber in driversToCompare:
        responseLength = urlopen('https://api.openf1.org/v1/stints?session_key=9488&stint_number=2&driver_number='+drivernumber)
        dataLength=json.loads(responseLength.read().decode('utf-8'))
        dfLength=pd.DataFrame(dataLength)
        lap_End=int(dfLength['lap_end'])
        lap_Start=int(dfLength['lap_start'])
        response = urlopen('https://api.openf1.org/v1/laps?session_key=9488&driver_number='+drivernumber)
        data=json.loads(response.read().decode('utf-8'))
        df=pd.DataFrame(data)
        df=df.loc[((df['lap_number']) > lap_Start) & ((df['lap_number']) < lap_End)]
        df=df[['lap_duration','driver_number']]
        mainDF=pd.concat([mainDF,df])
        
    
    mainDF.insert(0,'Total_Laps',np.arange(mainDF.shape[0]),True)
    
    return(mainDF)

def GraphGetStintsToCompare():
    time.sleep(5)
    g = sns.lmplot(data=getStintToCompare(),x="Total_Laps", y="lap_duration", hue="driver_number",height=5,palette=IntSetDriverColors(),robust=True)
    my_file4 = 'AustraliaTyreLifeComparison.png'
    plt.savefig(os.path.join(my_path, my_file4),dpi=300) 


######################################################


#GraphGetIntervalToLeader()
GraphGetStintsToCompare()
GraphTopSpeed()
GraphGetStints()

