from kafka import KafkaConsumer  
from kafka import KafkaProducer
import json
import time
import pandas as pd
import requests
import credentials #storing keys & credentials
from utils import deserializer,get_polygon_center

stations_url=f'{credentials.root}/id/stations'

areas_stations_cache={} # cache dict to save the previous fetched area-station mappings


def list_stations_for_flood_area(floodareaID,polygon_url):
    if floodareaID in areas_stations_cache:
        return areas_stations_cache[floodareaID]
    else:
        polygon=requests.get(polygon_url).json()
        
        center_lon,center_lat=get_polygon_center(polygon)#get approx center point for the flooding area 
        
        stations_parm={'lat':center_lat,
                       'long':center_lon,
                       'dist':20}#radius to search within
        stations=requests.get(stations_url,params=stations_parm).json()['items'] #get stations in 20km distance from the area's centerpoint
        areas_stations_cache[floodareaID] = [station ['stationReference'] for station in stations] #save areaID-stationsRefrences pairs
        return areas_stations_cache[floodareaID]
        
        
        
        
        

print(list_stations_for_flood_area('061FAG23HenAssen',"http://environment.data.gov.uk/flood-monitoring/id/floodAreas/061FAG23HenAssen/polygon"))



analytics_consumer= KafkaConsumer(
                               bootstrap_servers=credentials.server,                           
                               group_id='analytical_consumers',
                               value_deserializer=deserializer,
                               auto_offset_reset='latest'
                               )
analytics_consumer.subscribe([credentials.warnings_topic,credentials.measures_topic]) # fetch  data from both warnings and measures topics


warnings=[]
measures=[]

for message in analytics_consumer:
    if message.topic ==credentials.measures_topic:
        measures.append(message.value)
        
    elif message.topic==credentials.warnings_topic:
        warnings.append(message.value)
        
        
    if len(warnings)>0 and len(measures)>0:
        
        warnings_df=pd.DataFrame(warnings)
        warnings_df.rename(columns={'@id':'warning_id','eaAreaName':'AreaName'},inplace=True)
        measures_df=pd.DataFrame(measures)
        measures_df.rename(columns={'@id':'reading_id','dateTime':'TimeStamp'},inplace=True)

        warnings_df['responsible_station']=warnings_df.apply( lambda row: list_stations_for_flood_area(row['floodAreaID'],row['polygon']),axis=1) #get the stations responsible for each warning
        warnings_df=warnings_df.explode('responsible_station')
        analytics_df=pd.merge(measures_df,warnings_df,left_on='stationReference',right_on='responsible_station') #join two df on the station code
        #print(analytics_df.columns)
        analytics_df=analytics_df[['warning_id','reading_id','responsible_station','TimeStamp','country','AreaName','isTidal','floodAreaID','parameterName','value','unit','severity']] 
        analytics_df.to_csv('sample-analytical-table.csv')
        upload_df_to_s3(analytics_df,bucket=credentials.bucket_name,key=credentials.key)
        
        warnings.clear()
        measures.clear() #clearing data after each stream processing
        time.sleep(900)
