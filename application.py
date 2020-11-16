import requests
import json
import urllib
import sys
import logging
import folium
from flask import Flask, request, redirect, render_template

# creating instance of flask
app = Flask(__name__)

API_KEY = '22f223033b0eb05730a22bb57c63f606'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def weathermap():
    return render_template("map.html")

@app.route("/search")
def search_city():
    # base = 'https://api.openweathermap.org/data/2.5/weather?'

    # city name passed as arg
    city = request.args.get("city")
    
    # calling API and converting response into Python dict
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial,metric&APPID={API_KEY}'
    response = requests.get(url).json()

    # if not city:
    #     return render_template("failure.html")

    # error if city not found 
    if response.get('cod') != 200:
        msg = response.get('msg', '')
        return f'Error getting current temperature of {city.title()}. {msg}'

    # accessing dict by keys with get method and converting temp from K to F and C
    current_temp = response.get('main', {}).get('temp')
    if current_temp:
        current_temp_f = round((current_temp - 273.15)*1.8+32, 2)
        current_temp_c = round(current_temp - 273.15, 2)
        return render_template("search.html", city=city, current_temp_f=current_temp_f, current_temp_c=current_temp_c)
    else:
        return f'Error retrieving temperature for {city.title()}'
        #return render_template("search.html", city=city)

if __name__=='__main__':
    app.run(debug=True, )