from kafka import KafkaProducer
import json
import time
import pandas as pd
import requests
import credentials #scripts that retrieves all keys & credentials


warnings_url=f'{credentials.root}/id/floods'
#print(warnings_url)

response=requests.get(url=warnings_url)

if response.status_code==200:

    data=response.json()['items']
    warnings=pd.DataFrame(data)
    
    #transformations
    warnings['country'],warnings['polygon']=warnings['floodArea'].apply(lambda  x :x['county']) , warnings['floodArea'].apply(lambda x: x['polygon'])
    warnings=warnings[['@id','timeRaised','eaAreaName','description','country','floodAreaID','polygon','isTidal','message','severity']]  
    

else :
    print(f"Error Fetching Data From {warnings_url} ")
    




def serializer(data_row):
  if data_row is not None:
      data_row=data_row.to_dict()
      return json.dumps(data_row).encode('utf-8')
  else:
      return None



warnings_producer=KafkaProducer(bootstrap_servers=credentials.server,
                                value_serializer=serializer,
                                client_id='warnings_producer-1')  #streams flood warnings


for _,row in warnings.iterrows():
    
    warnings_producer.send(topic=credentials.warnings_topic,value=row)
    warnings_producer.flush()
    print(f"sent warnings for : {row['eaAreaName']}")
    time.sleep(15)
    
