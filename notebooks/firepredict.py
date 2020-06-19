import os
import config

import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import time
import threading

from datetime import date
from datetime import datetime
from datetime import timedelta
from darksky import forecast


import ipywidgets as widgets
from ipywidgets import TwoByTwoLayout
from ipywidgets import GridspecLayout
from IPython.display import display, HTML


RAPIDAPI_KEY  = config.darksky_api1

#Loading Models and Data
df_fires = pd.read_csv('data/FireIntensity_Model_June12_Clean.csv')


#Defining widgets
datepicker = widgets.DatePicker(
    description='Fire start: ',
    disabled=False,
    value = date.today()
)

temperature = widgets.IntSlider(value=85, max=120, min=20, description='Temperature: ')
temperature.style.handle_color = 'lightblue'

humidity = widgets.IntSlider(value=85, max=120, min=20, description='Humidity: ')

lat = widgets.FloatSlider(value=df_fires.latitude.median(),
                          max=df_fires.latitude.max(),
                          min=df_fires.latitude.min(),
                          description='Latitude: ',
                          readout_format='.4f',
                          step=0.0001,
                         )
lat.style.handle_color = 'lightpink'

lon = widgets.FloatSlider(value=df_fires.longitude.median(),
                          max=df_fires.longitude.max(),
                          min=df_fires.longitude.min(),
                          description='Longitude: ',
                          readout_format='.4f',
                          step=0.0001,
                         )
lon.style.handle_color = 'lightpink'

fuel_moist = widgets.Dropdown(
    options=[('Very Dry', 1), ('Dry', 2), ('Moderate', 3), ('Moist', 4)],
    value=1,
    description='Fuel Moisture Class:',
)

prefire = widgets.FloatSlider(value=df_fires.prefire_fuel.median(),
                          max=df_fires.prefire_fuel.max(),
                          min=df_fires.prefire_fuel.min(),
                          description='Prefire Fuel: ',
                          readout_format='.5f',
                          step=0.00001,
                         )
prefire.style.handle_color = 'lightblue'

fuel_code = widgets.Dropdown(
    options=[('Herbaceous ', 1), 
             ('Shrub / scrub ', 2),
             ('Spruce / fir group ', 1120), 
             ('Longleaf / slash pine group ', 1140), 
             ('Loblolly / shortleaf pine group ', 1160), 
             ('Douglas-fir group ', 1200), 
             ('Hemlock / Sitka spruce group ', 1300), 
             ('Redwood group ', 1340), 
             ('Oak / hickory group ', 1500), 
             ('Elm / ash / cottonwood group ', 1700)],
    value=1,
    description='Cover Type:',
)

button = widgets.Button(description="Predict Fire")
output = widgets.Output()

# display(button, output)

def on_button_clicked(b):
    with output:
        print("Warming up...")
#         print("Finding region on map...")
#         def haversine_distance(lat1, lon1, lat2, lon2):
#             r = 6371
#             phi1 = np.radians(lat1)
#             phi2 = np.radians(lat2)
#             delta_phi = np.radians(lat2 - lat1)
#             delta_lambda = np.radians(lon2 - lon1)
#             a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
#             res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
#             return np.round(res, 2)

#         distances_km = []

#         for row in df_fires.itertuples(index=False):
#             distances_km.append(
#             haversine_distance(lat.value, lon.value, row.latitude, row.longitude)
#          )

#         df_fires['DistanceFromPoint'] = distances_km

#         fire_region_in = df_fires[df_fires.DistanceFromPoint == df_fires.DistanceFromPoint.min()].fire_region.min()
#         print('### remove this ###  Region: ',fire_region_in)
        
        #get season input
        def get_season(doy):
            if ((doy >= 80) and (doy <= 172)):
                s = 0  # spring
            elif ((doy > 172) and (doy < 264)):
                s = 1  # summer
            elif ((doy >= 264) and (doy <= 355)):
                s = 2  # fall
            #elif ((doy > 355) and (doy < 80)):
                #s = 3  # winter
            else:
                s = 3
             #   raise IndexError("Invalid date")
            return s
        
        season_in = get_season(datepicker.value.timetuple().tm_yday)
        print('### remove this ###  Season: ',season_in)
        
        
        print("Pulling weather data from DarkSky...")
        def weather_lookup(df, key=RAPIDAPI_KEY, days_before=0, days_after=0):
            data = []
            for index, row in df.iterrows():
                ts = row['datetime'].isoformat() 
                lat = row['latitude']
                lon = row['longitude']
                weather = forecast(key, lat, lon, time=ts)
                w_dict = weather['currently']
                w_dict['timestamp'] = ts
                w_dict['latitude'] = lat
                w_dict['longitude'] = lon
                data.append(w_dict)
            return data
        
        dt = datetime(datepicker.value.year, datepicker.value.month, datepicker.value.day, 12)
        fire_predict = pd.DataFrame(columns=['datetime', 'latitude', 'longitude'])
        fire_predict = fire_predict.append({'datetime': dt, 'latitude': lat.value, 'longitude': lon.value}, ignore_index=True)
        weather_df = pd.DataFrame(weather_lookup(fire_predict))
        
        temperature_in = weather_df.temperature.min()
        wind_speed_in = weather_df.windSpeed.min()
        humidity_in = weather_df.humidity.min()
        precip_intensity_in = weather_df.precipIntensity.min()
        wind_gust_in = weather_df.windGust.min()
        
        print('### remove this ###  Weather Data: ')
        print("Temperature: ", temperature_in)
        print("Humidity: ", humidity_in)
        print("Precip Intensity: ", precip_intensity_in)
        print("Wind Gust: ", wind_gust_in)
        print("Wind Speed: ", wind_speed_in)
        
        print("Calculating Intinsity...")
        
        print("Fire is SEVERE!")

fireapp = GridspecLayout(4, 3)
fireapp[0,0] = datepicker
fireapp[1,0] = lat
fireapp[2,0] = lon
fireapp[0,1] = fuel_moist
fireapp[1,1] = fuel_code
fireapp[2,1] = prefire
fireapp[0,2] = button

fire = display(fireapp, output)

button.on_click(on_button_clicked)
display(output)