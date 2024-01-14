# this script runs from crontab using setting below
# */1 * * * * python /var/www/html/bus.py
# this page is being served by a RPi on the same network as the nook
# the nook then calls this html page and uses "electic sign" to save as screensaver
# screensaver is set to update once a minute
# i only request weather data once an hour to reduce api calls to openweather
# DW Jan 2024 - based on edent example at
# https://shkspr.mobi/blog/2020/02/turn-an-old-ereader-into-an-information-screen-nook-str/

import requests
import json
from datetime import datetime

# Function to fetch data from the API's
def fetch_bus():
    try:
        response = requests.get('https://api.tfl.gov.uk/StopPoint/490003212S/arrivals')
        data = response.json()
        return data
    except Exception as e:
        print('Error fetching data:', e)

def fetch_weather():
    try:
        response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid=xxx')
        data = response.json()
        return data
    except Exception as e:
        print('Error fetching weather data:', e)

def fetch_carbon():
    try:
        response = requests.get('https://api.carbonintensity.org.uk/intensity')
        data = response.json()
        return data
    except Exception as e:
        print('Error fetching carbon data:', e)

# Function to convert seconds to minutes and seconds
def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f'{minutes} min' # {remaining_seconds} sec'

def get_bus_html():
    bus_data = fetch_bus()
    table_rows = []

    if len(bus_data):
        # Sort bus_data list by timeToStation
        bus_data.sort(key=lambda x: x['timeToStation'])

        # Loop through the sorted bus predictions and create an array of information
        for prediction in bus_data:
            destination = prediction['destinationName']
            line_name = prediction['lineName']
            time_to_station = format_time(prediction['timeToStation'])
            vehicle_Id  = prediction['vehicleId']

            table_row = f'<tr><td width=12% align=right><strong>{line_name}</strong></td><td width=23% align=right>{time_to_station}</td><td align=right>{destination}</td><td width=20% style="font-size: 0.7em;">{vehicle_Id}</td></tr>'
            table_rows.append(table_row)

        # Combine the table rows into a table
        table_content = f'<table width=100% style="font-size: 1em;">{"".join(table_rows)}</table>'
    else:
        table_content = f'<p>No buses on the horizon...</p>'
    
    return(table_content)

def get_time_html():
    # Add timestamp with the current date and time
    timestamp = datetime.now().strftime('%H:%M:%S')
    timestamp_content = f'<p>Last checked: {timestamp}</p>'
    return(timestamp_content)

def get_weather_html():
    
    current_time = datetime.now()
    if current_time.minute < 3:

        # get weather data
        weather_data = fetch_weather()

        # Extract relevant information
        city_name = weather_data['name']
        temperature = weather_data['main']['temp']
        tempfeels = weather_data['main']['feels_like']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        icon_code = weather_data['weather'][0]['icon']

        # Convert sunrise and sunset times to human-readable format
        sunrise_timestamp = weather_data['sys']['sunrise']
        sunset_timestamp = weather_data['sys']['sunset']

        sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H:%M')
        sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime('%H:%M')


        # Format into a human-readable string with HTML formatting
        # f"<p><img src='http://openweathermap.org/img/w/{icon_code}.png' alt='Weather Icon'></p>" \
        result_html = f"<p>{city_name}: {temperature:.0f}&deg;C (feels like {tempfeels:.0f}&deg;C)</p>" \
                    f"<p>H: {humidity}% Wind: {wind_speed} m/s P: {pressure}hPa</p>" \
                    f"<p>Forecast: {description}</p>" \
                    f"<p><strong>Sunrise:</strong> {sunrise_time} <strong>Sunset:</strong> {sunset_time}</p>"

        # Write the content to a file
        with open('/var/www/html/weather.html', 'w', encoding='utf-8') as file:
            file.write(result_html)
    
    else:
        
        with open('/var/www/html/weather.html', 'r', encoding='utf-8') as file:
            result_html = file.read()

    return(result_html)

def get_carbon_html():
    carbon_data = fetch_carbon()
    actual_intensity = carbon_data['data'][0]['intensity']['actual']
    intensity_index = carbon_data['data'][0]['intensity']['index']
    carbon_html = f"<p>Carbon Intensity: {actual_intensity} gCO2/kWh<br>" \
                f"Intensity Index: {intensity_index}</p>"

    return(carbon_html)



# Function to display bus information and save to a file
def save_to_file():
    
    bus_html = get_bus_html()
    updated_html = get_time_html()
    weather_html = get_weather_html()
    carbon_html = get_carbon_html()

    # Combine the array into a single string
    content = f'<html><head><title>Bus Arrival Information</title>' \
        f'<style>body{{margin: 20px; border: 20px solid white; box-sizing: border-box; font-size: 2em;}}</style></head>' \
        f'<body>{updated_html}<p><strong>CQ</strong> towards Highgate</p>{bus_html}{weather_html}{carbon_html}</body></html>'

    # Write the content to a file
    with open('/var/www/html/bus.html', 'w', encoding='utf-8') as file:
        file.write(content)

    print('File saved successfully: bus_arrival_information.html')

# Run the save_to_file function
save_to_file()
