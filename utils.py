import folium
import json
import threading
import boto3
from io import StringIO
import  credentials



def update_map(coords_list):
    global current_map
    current_map = folium.Map(location=[51.5, -0.1], zoom_start=7)

    for polygon in coords_list:
        feature = polygon.get("features", [])[0]
        geometry = feature.get("geometry", {})
        poly_coords = geometry.get("coordinates", [])
        poly_type = geometry.get("type", "")

        if poly_type == "MultiPolygon":
            for poly in poly_coords:
                for ring in poly:
                    folium.Polygon(
                        locations=[[lat, lon] for lon, lat in ring],
                        color='red',
                        weight=10,
                        opacity=0.9,
                        fill=True,
                        fill_color='red',
                        fill_opacity=0.9
                    ).add_to(current_map)
                    print("Added a MultiPolygon ring")

        elif poly_type == "Polygon":
            for ring in poly_coords:
                folium.Polygon(
                    locations=[[lat, lon] for lon, lat in ring],
                    color='red',
                    weight=10,
                    opacity=0.9,
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.9
                ).add_to(current_map)
                print("Added a Polygon ring")



def serializer(data_row):
  if data_row is not None:
      data_row=data_row.to_dict()
      return json.dumps(data_row).encode('utf-8')
  else:
      return None




def deserializer(byte):
    return json.loads(byte.decode('utf-8'))

def get_polygon_center(polygon_response):
            all_coords = []
            for feature in polygon_response.get('features', []):
                if feature['geometry']['type'] == 'MultiPolygon':
                    for polygon in feature['geometry']['coordinates']:
                        for ring in polygon:  # First ring is the outer boundary
                            all_coords.extend(ring)
            
            if not all_coords:
                print(f"No coordinates found for area {polygon_response}")
                return []
            
            # Calculate centroid by averaging all coordinates
            lons = [coord[0] for coord in all_coords]
            lats = [coord[1] for coord in all_coords]
            centroid_lon = sum(lons) / len(lons)
            centroid_lat = sum(lats) / len(lats)
            return centroid_lon,centroid_lat
        
        
        
def upload_df_to_s3(df, bucket, key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=credentials.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=credentials.AWS_SECRET_ACCESS_KEY
    )
    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer.getvalue()
    )
    return True