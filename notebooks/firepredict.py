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

# Darksky API Key
RAPIDAPI_KEY  = config.darksky_api1


# Defining widgets

# Date Picker for selecting the day
datepicker = widgets.DatePicker(
    description='Fire start: ',
    disabled=False,
    value = date.today()
)

# Temperature slider, not needed if DarkSky is working
temperature = widgets.IntSlider(value=85, max=120, min=20, description='Temperature: ')
temperature.style.handle_color = 'lightblue'

# Humidity slider, not needed if DarkSky is working
humidity = widgets.IntSlider(value=85, max=120, min=20, description='Humidity: ')

# Latitude slider
lat = widgets.FloatSlider(value=35.9013,
                          max=48.9926,
                          min=24.5457,
                          description='Latitude: ',
                          readout_format='.4f',
                          step=0.0001,
                         )
lat.style.handle_color = 'lightpink'

# Longitude slider
lon = widgets.FloatSlider(value=-96.2438,
                          max=-67.0042,
                          min=-124.6325,
                          description='Longitude: ',
                          readout_format='.4f',
                          step=0.0001,
                         )
lon.style.handle_color = 'lightpink'

# Fuel Moisture Picker
fuel_moist = widgets.Dropdown(
    options=[('Very Dry', 1), ('Dry', 2), ('Moderate', 3), ('Moist', 4)],
    value=1,
    description='Moisture: ',
)

# Prefire fuel slider
prefire = widgets.FloatSlider(value=4335.068543,
                          max=13337.51083,
                          min=19.61505,
                          description='Prefire Fuel: ',
                          readout_format='.5f',
                          step=0.00001,
                         )
prefire.style.handle_color = 'lightblue'

# Cover Type Picker
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

# Creating Button and Output to start prediction
button = widgets.Button(description="Predict Fire")
output = widgets.Output()

# Widget used to clear results
clear = widgets.Button(description="Clear Results")
def clear_results(b):
    with output:
        output.clear_output()
clear.on_click(clear_results)

# Function to determind what happens when Predict Fire button is clicked
def on_button_clicked(b):
    with output:
        print("Warming up...")
        print("Finding season...")  

        #getting season input
        def get_season(doy):
            if ((doy >= 80) and (doy <= 172)):
                s = 0  # spring
            elif ((doy > 172) and (doy < 264)):
                s = 1  # summer
            elif ((doy >= 264) and (doy <= 355)):
                s = 2  # fall
            else:
                s = 3 # winter
            return s
        
        # Setting the season input value from datepicker
        season_in = get_season(datepicker.value.timetuple().tm_yday)
        
        # Pull weather info from DarkSky API
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
        
        # creating dataframe with weather info
        dt = datetime(datepicker.value.year, datepicker.value.month, datepicker.value.day, 12)
        fire_predict = pd.DataFrame(columns=['datetime', 'latitude', 'longitude'])
        fire_predict = fire_predict.append({'datetime': dt, 'latitude': lat.value, 'longitude': lon.value}, ignore_index=True)
        weather_df = pd.DataFrame(weather_lookup(fire_predict))
        
        # Set outputs from DarkSky API as variables
        temperature_in = weather_df.temperature.min()
        wind_speed_in = weather_df.windSpeed.min()
        humidity_in = weather_df.humidity.min()
        precip_intensity_in = weather_df.precipIntensity.min()
        wind_gust_in = weather_df.windGust.min()
        
        # function to open estimator & define X
        def open_estimator(filename) :
    
            infile = open(filename,'rb')
            estimator = pickle.load(infile)
            infile.close()
        
            print ("Model Loaded...")
            return estimator
        
        def find_X (df):
        
            features = ['latitude', 'longitude', 'doy','fuelcode', 'fuel_moisture_class', 'prefire_fuel', 'temperature', 'humidity', 'precip_intensity', 
                     'wind_gust', 'wind_speed']
            X = df[features]
            return X

        # load model    
        model = open_estimator("pipeline.pickle")

        
        #setting dataframe & X variables
        app_inputs = pd.DataFrame(columns=['latitude', 'longitude', 'doy','fuelcode', 'fuel_moisture_class', 'prefire_fuel', 'temperature', 'humidity', 'precip_intensity', 
             'wind_gust', 'wind_speed'])

        app_inputs = app_inputs.append({'latitude': lat.value,
                                'longitude': lon.value,
                                'doy': datepicker.value.timetuple().tm_yday,
                                'fuelcode': fuel_code.value,
                                'fuel_moisture_class': fuel_moist.value,
                                'prefire_fuel': prefire.value,
                                'temperature': temperature_in,
                                'humidity': humidity_in,
                                'precip_intensity': precip_intensity_in,
                                'wind_gust': wind_gust_in,
                                'wind_speed': wind_speed_in},
                               ignore_index=True)
        X = find_X(app_inputs)
        print("Inputs Loaded...")

        # Calculating Model Results
        print("Calculating Intinsity...")
        predicted = model.predict(X)
        print("")

        # Print out Inputs
        print("------Model Input Values------")
        print("Latitude: ", lat.value)
        print("Longitude: ", lon.value)
        print("Day of Year: ", datepicker.value.timetuple().tm_yday)
        print("Fuelcode: ", fuel_code.value)
        print("Fuel Moisture Class: ", fuel_moist.value)
        print("Prefire Fuel: ", prefire.value)
        print("Temperature: ", temperature_in)
        print("Humidity: ", humidity_in)
        print("Precip Intensity: ", precip_intensity_in)
        print("Wind Gust: ", wind_gust_in)
        print("Wind Speed: ", wind_speed_in)
        print("-------------------------------")
        print("")
        print("----------------")
        print("|   ",predicted[0],"   |")
        print("----------------")
        print("")
        print("")

button.on_click(on_button_clicked)

# Setting the grid layout for the app
fireapp = GridspecLayout(50, 3)
fireapp[0,0] = datepicker
fireapp[1,0] = lat
fireapp[2,0] = lon
fireapp[0,1] = fuel_moist
fireapp[1,1] = fuel_code
fireapp[2,1] = prefire
fireapp[0,2] = button
fireapp[1,2] = clear
fireapp[3:,0:] = output
