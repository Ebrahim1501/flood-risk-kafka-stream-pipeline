from kafka import KafkaConsumer  
from flask import Flask, render_template_string
import json
import requests
import folium
import threading
import credentials  # custom file with Kafka credentials(hidden)
from utils import update_map #this py file contains all  utility functions needed in the application  

app = Flask(__name__)

coordinates = []
lock = threading.Lock()

current_map = folium.Map(location=[51.5, -0.1], zoom_start=7) #---------------> intial plain map with no polygons

def deserializer(byte):
    return json.loads(byte.decode('utf-8'))








def consume_warnings():
    
    consumer = KafkaConsumer(
        credentials.warnings_topic,
        bootstrap_servers=credentials.server,
        group_id='warning_handlers_consumers',
        value_deserializer=deserializer,
        auto_offset_reset='latest'
    )

    for message in consumer:
        data = message.value
        response = requests.get(data['polygon'])

        if response.status_code == 200:
            print(f"Fetched Coordinates Successfully From {data['polygon']}")
            polygon = response.json()

            polygon["properties"] = {"floodArea": data.get("floodArea", "Flood Warning Area")} # for debugging only 2 be removed later

            with lock:
                coordinates.append(polygon)
                update_map(coordinates) #function used to display current warning areas over the map
                print(f"Updated the map with coordinated for {data['eaAreaName']}")
        else:
            print(f"Error Fetching Coordinates from {data['polygon']}")

@app.route("/")
def index():
    with lock:
        map_html = current_map._repr_html_()
    
    return render_template_string("""
        <html>
            <head>
                <title>Warning Polygon Map</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
                    #map { height: 100vh; width: 100%; }
                </style>
            </head>
            <body>
                <div id="map">{{ map_html|safe }}</div>
            </body>
        </html>
    """, map_html=map_html)


if __name__ == "__main__":
    consumer_thread = threading.Thread(target=consume_warnings, daemon=True) #---> seperate thread to enable map rendering outside the kafka's loop
    consumer_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
