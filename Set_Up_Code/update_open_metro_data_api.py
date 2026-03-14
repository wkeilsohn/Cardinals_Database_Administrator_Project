import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import date, datetime

# Change parameters

def prep_dates(last_date):
	today = date.today()
	if last_date[0] < today:
		end_date = "2026-0{}-{}".format(str(today.month), str(today.day + 7))
		start_date = last_date + timedelta(days=1)
		start_date = f"{start_date:%Y-%m-%d}"
		print(start_date)
		return(start_date, end_date)
	else:
		return []

def client_setup():
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

def call_api(start_date, end_date):
	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 36.62,
		"longitude": -90.91,
		"daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours"],
		"timezone": "America/Chicago",
		"wind_speed_unit": "mph",
		"temperature_unit": "fahrenheit",
		"precipitation_unit": "inch",
		"start_date": start_date,
		"end_date": end_date,
	}
	responses = openmeteo.weather_api(url, params=params)
	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	return response

def process_data(resp):
	# Process daily data. The order of variables needs to be the same as requested.
	daily = resp.Daily()
	daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
	daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
	daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
	daily_rain_sum = daily.Variables(4).ValuesAsNumpy()
	daily_showers_sum = daily.Variables(5).ValuesAsNumpy()
	daily_snowfall_sum = daily.Variables(6).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(7).ValuesAsNumpy()
	daily_precipitation_hours = daily.Variables(8).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}

	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
	daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
	daily_data["rain_sum"] = daily_rain_sum
	daily_data["showers_sum"] = daily_showers_sum
	daily_data["snowfall_sum"] = daily_snowfall_sum
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["precipitation_hours"] = daily_precipitation_hours

	update_weather_df = pd.DataFrame(data = daily_data)
	return update_weather_df