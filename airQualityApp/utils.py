import json
import os
from datetime import datetime


def air_quality_category(pollutant, concentration):
    if pollutant == 'o3':
        if concentration <= 54:
            return 1
        elif concentration <= 70:
            return 2
        elif concentration <= 85:
            return 3
        elif concentration <= 105:
            return 4
        elif concentration <= 200:
            return 5

    elif pollutant == 'no2':
        if concentration <= 53:
            return 1
        elif concentration <= 100:
            return 2
        elif concentration <= 360:
            return 3
        elif concentration <= 649:
            return 4
        elif concentration <= 1249:
            return 5


    elif pollutant == 'so2':
        if concentration <= 35:
            return 1
        elif concentration <= 75:
            return 2
        elif concentration <= 185:
            return 3
        elif concentration <= 304:
            return 4
        elif concentration <= 604:
            return 5

    elif pollutant == 'co':
        if concentration <= 440:
            return 1
        elif concentration <= 940:
            return 2
        elif concentration <= 1240:
            return 3
        elif concentration <= 1540:
            return 4
        elif concentration <= 3040:
            return 5

    elif pollutant == 'pm25':
        if concentration <= 12.0:
            return 1
        elif concentration <= 35.4:
            return 2
        elif concentration <= 55.4:
            return 3
        elif concentration <= 150.4:
            return 4
        elif concentration <= 250.4:
            return 5

    elif pollutant == 'pm10':
        if concentration <= 54:
            return 1
        elif concentration <= 154:
            return 2
        elif concentration <= 254:
            return 3
        elif concentration <= 354:
            return 4
        elif concentration <= 424:
            return 5

    else:
        return 0


def aqi_level(aqi):
    if aqi <= 50:
        return 1
    elif aqi <= 100:
        return 2
    elif aqi <= 150:
        return 3
    elif aqi <= 200:
        return 4
    elif aqi <= 300:
        return 5


def process_environmental_index(name):
    if name == 'h': return 'Humidity'
    if name == 'p': return 'Pressure'
    if name == 't': return 'Temperature'
    if name == 'w': return 'Wind'
    if name == 'pm25': return 'PM2.5'
    if name == 'wg': return 'Wind Gust'
    if name == 'pm10': return 'PM10'
    if name == 'co': return 'CO'
    if name == 'no2': return 'NO2'
    if name == 'o3': return 'O3'
    if name == 'so2': return 'SO2'
    if name == 'co2': return 'CO2'
    if name == 'dew': return 'DEW'
    return name


# 读取JSON数据的函数
def load_json_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return []


# 写入JSON数据到文件的函数
def save_json_data(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
