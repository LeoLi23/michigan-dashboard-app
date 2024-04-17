import concurrent
import requests
from .utils import *
from django.conf import settings
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

# all cities in south michigan and their coordinates
cities = [
    {'city': 'Benton Harbor', 'coordinates': {'lat': 42.1167, 'lng': -86.4542}},
    {'city': 'South Haven', 'coordinates': {'lat': 42.4036, 'lng': -86.2733}},
    {'city': 'Kalamazoo', 'coordinates': {'lat': 42.2917, 'lng': -85.5872}},
    {'city': 'Saugatuck', 'coordinates': {'lat': 42.6556, 'lng': -86.2014}},
    {'city': 'Lansing', 'coordinates': {'lat': 42.7325, 'lng': -84.5555}},
    {'city': 'Battle Creek', 'coordinates': {'lat': 42.3211, 'lng': -85.1797}},
    {'city': 'Grand Haven', 'coordinates': {'lat': 43.0631, 'lng': -86.2284}},
    {'city': 'Holland', 'coordinates': {'lat': 42.7875, 'lng': -86.1089}},
    {'city': 'Detroit', 'coordinates': {'lat': 42.3314, 'lng': -83.0458}},
    {'city': 'St. Clair Shores', 'coordinates': {'lat': 42.4974, 'lng': -82.8964}},
    {'city': 'Southfield', 'coordinates': {'lat': 42.4734, 'lng': -83.2219}},
    {'city': 'Southgate', 'coordinates': {'lat': 42.2133, 'lng': -83.2084}},
    {'city': 'South Lyon', 'coordinates': {'lat': 42.4614, 'lng': -83.6509}},
    {'city': 'Swartz Creek', 'coordinates': {'lat': 42.9573, 'lng': -83.8303}},
    {'city': 'Scottville', 'coordinates': {'lat': 43.9553, 'lng': -86.2740}},
    {'city': 'Ann Arbor', 'coordinates': {'lat': 42.2808, 'lng': -83.7430}},
    {'city': 'Sturgis', 'coordinates': {'lat': 41.7992, 'lng': -85.4192}},
    {'city': 'Sebewaing', 'coordinates': {'lat': 43.7325, 'lng': -83.4301}},
    {'city': 'St. Ignace', 'coordinates': {'lat': 45.8683, 'lng': -84.7225}},
    {'city': 'Springport', 'coordinates': {'lat': 42.3828, 'lng': -84.7430}},
    {'city': 'Sunfield', 'coordinates': {'lat': 42.7686, 'lng': -84.9814}},
    {'city': 'Suttons Bay', 'coordinates': {'lat': 44.9754, 'lng': -85.6483}},
    {'city': 'Sandusky', 'coordinates': {'lat': 43.4094, 'lng': -82.8234}},
    {'city': 'Traverse City', 'coordinates': {'lat': 44.7631, 'lng': -85.6206}},
    {'city': 'Hamtramck', 'coordinates': {'lat': 42.3926, 'lng': -83.0496}},
    {'city': 'Berkley', 'coordinates': {'lat': 42.5031, 'lng': -83.1837}},
    {'city': 'Highland Park', 'coordinates': {'lat': 42.3926, 'lng': -83.0890}},
    {'city': 'Dearborn Heights', 'coordinates': {'lat': 42.3361, 'lng': -83.2733}},
    {'city': 'Farmington', 'coordinates': {'lat': 42.4645, 'lng': -83.3763}},
    {'city': 'Ecorse', 'coordinates': {'lat': 42.2446, 'lng': -83.1392}},
    {'city': 'Saint Charles', 'coordinates': {'lat': 43.2861, 'lng': -84.1236}},
    {'city': 'East Lansing', 'coordinates': {'lat': 42.7360, 'lng': -84.4839}},
    {'city': 'Ypsilanti', 'coordinates': {'lat': 42.2411, 'lng': -83.6129}},
    {'city': 'Rockford', 'coordinates': {'lat': 43.1200, 'lng': -85.5600}},
    {'city': 'Dearborn', 'coordinates': {'lat': 42.3223, 'lng': -83.1763}},
    {'city': 'Novi', 'coordinates': {'lat': 42.4801, 'lng': -83.4755}},
    {'city': 'Sterling Heights', 'coordinates': {'lat': 42.5803, 'lng': -83.0302}},
    {'city': 'Farmington Hills', 'coordinates': {'lat': 42.4982, 'lng': -83.3677}},
    {'city': 'Auburn Hills', 'coordinates': {'lat': 42.6875, 'lng': -83.2341}},
    {'city': 'Wyandotte', 'coordinates': {'lat': 42.2042, 'lng': -83.1499}},
    {'city': 'Alpena', 'coordinates': {'lat': 45.0617, 'lng': -83.4327}},
    {'city': 'Coldwater', 'coordinates': {'lat': 41.9403, 'lng': -85.0006}},
    {'city': 'Port Huron', 'coordinates': {'lat': 42.9826, 'lng': -82.4387}}
]
# AQI API TOKEN from settings.py
TOKEN = settings.TOKEN


# fetch AQI data for specific city from API
def fetch_api_data(city):
    # get city coordinates
    lat = city['coordinates']['lat']
    lng = city['coordinates']['lng']
    # get data from API
    url = f'https://api.waqi.info/feed/geo:{lat};{lng}/?token={TOKEN}'
    response = requests.get(url)
    data = response.json()
    # process data
    current_data = {
        "AQI": [data["data"]["aqi"], aqi_level(data["data"]["aqi"])],
    }
    # process environmental index
    for key in data["data"]["iaqi"].keys():
        processed_key = process_environmental_index(key)
        if key not in current_data.keys():
            current_data[processed_key] = [data["data"]["iaqi"][key]["v"],
                                           air_quality_category(key, data["data"]["iaqi"][key]["v"])]
    # process future data
    future_data = {
        "O3": data["data"]["forecast"]["daily"]["o3"],
        "PM10": data["data"]["forecast"]["daily"]["pm10"],
        "PM2.5": data["data"]["forecast"]["daily"]["pm25"]
    }
    # return data
    return {"cityName": city['city'], "lat": lat, "lng": lng,
            "current_data": current_data, "future_data": future_data}


# fetch all cities data from API, process them and save to JSON file
def fetch_api_data_and_process():
    results = []
    # fetch data from API using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_all_api = {executor.submit(fetch_api_data, city): city for city in cities}
        for future in concurrent.futures.as_completed(future_to_all_api):
            all_api_data = future.result()
            results.append(all_api_data)

    # save data to JSON file
    json_results = json.dumps(results, cls=DjangoJSONEncoder)
    return json_results


# view for map
def mapView(request):
    # get data from cache
    filepath = os.path.join(settings.BASE_DIR, 'airQualityApp/data.json')
    data_list = load_json_data(filepath)
    # get today's date
    today_str = datetime.now().strftime("%Y-%m-%d")

    # check if data is in cache
    if data_list and data_list[-1].get("date") == today_str:
        print("Getting data from cache")
        # get data from cache
        result = data_list[-1].get("data")
    else:
        print("Asking new data")
        # get data from API
        result = fetch_api_data_and_process()
        data_list.append({"date": today_str, "data": result})
        # save data to cache
        save_json_data(filepath, data_list)

    # context for map
    context = {
        'title': 'Air Quality Index',
        'content': 'Welcome to the air quality index page.',
        'data': result
    }

    return render(request, 'airQualityApp/index.html', context)
