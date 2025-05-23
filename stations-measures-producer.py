from kafka import KafkaConsumer  
from kafka import KafkaProducer
import json
import time
import pandas as pd
import requests
import credentials #storing keys & credentials
from utils import serializer



measures_url=f"{credentials.root}/id/measures"


measures_producer=KafkaProducer(bootstrap_servers=credentials.server,value_serializer=serializer,client_id="metrics-producer-1")
measures_response=requests.get(measures_url,params={'_limit':500})



data=measures_response.json()['items']
# ls=[]
# print(len(stations))
#print(data[0])


while True:
    
    measures_response=requests.get(measures_url,params={'_limit':500})
    readings=measures_response.json()['items']
    df=pd.DataFrame(readings)
    df = df[df['latestReading'].apply(lambda x: isinstance(x, dict))].reset_index(drop=True) #filters data without readings


    df['readingID']=df['latestReading'].apply(lambda  x :x['@id'])
    df['dateTime']=df['latestReading'].apply(lambda  x :x['dateTime'])
    df['value']=df['latestReading'].apply(lambda  x :x['value'])
    readings_df=df[['@id','station','stationReference','dateTime','parameterName','value','unit']]
    

    for idx,reading in readings_df.iterrows():
        pending=measures_producer.send(credentials.measures_topic,reading)
        meta=pending.get(timeout=300)
        
        print(f"sent reading {idx} to The broker topic : {meta.topic} partition: {meta.partition}  ")
        
    print("Waiting For New Readings")
    time.sleep(900) # as the readings get updated every 15 minutes