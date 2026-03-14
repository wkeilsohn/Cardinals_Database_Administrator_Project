# William Keilsohn
# March 13, 2026

# Import Packages
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2 as psy
from sqlalchemy import create_engine

## Load Custom Files
from project_data import dba_project_data_df
from open_metro_api import daily_dataframe as weather_data_df
from update_open_metro_data_api import *
from mlb_data import mlb_data

# Load in Secrets
load_dotenv()

# Define Variables

## PostgreSQL Connection Related
address = "127.0.0.1" # Yes, in prod you should hide all of these, but this is a quick project and I'm running it on my local machine so it is what it is. 
port = "5432" # Also, yes, these are all default values. 
db_name = "postgres"
user_name = "postgres"
password = os.getenv("PASSWORD") # Too spicy not to hide. 
connection_string = "postgresql+psycopg2://postgres:{}@127.0.0.1:5432/postgres".format(password)
engine = create_engine(connection_string)
db = create_engine(connection_string)
conn1 = db.connect()

## Construction Queries
check_query = "SELECT to_regclass('public.{}') IS NOT NULL AS table_exists;"
check_row_query = "SELECT * FROM {};"
check_last_entry_query = "SELECT weather_data.date FROM weather_data ORDER BY date DESC LIMIT 1;"

### Table Creation Queries
table_dic = {'project_data': "CREATE TABLE IF NOT EXISTS project_data (snapshot_date date, game_date date, unique_tickets_sold int, unique_page_clicks int);",
'weather_data': "CREATE TABLE IF NOT EXISTS weather_data (date date, temperature_2m_max float, temperature_2m_min float, apparent_temperature_max float, apparent_temperature_min float, rain_sum float, showers_sum float, snowfall_sum float, precipitation_sum float, precipitation_hours float);",
'mlb_data': "CREATE TABLE IF NOT EXISTS mlb_data (game_date date);"}

# Declare Functions
def create_post_conn():
	global address
	global port
	global db_name
	global user_name
	global password
	conn = psy.connect(host=address, database=db_name, user=user_name, password=password, port=int(port))
	return conn

def check_post_conn(conn):
	if conn.closed == 0:
		# print("Connection is Open")
		return conn
	else:
		return create_post_conn()

def check_table_exists(table_name, cursor):
	global check_query
	table_query = check_query.format(table_name)
	cursor.execute(table_query)
	status = cursor.fetchone()[0]
	return status

def create_table(create_query, cursor, conn):
	cursor.execute(create_query)
	conn.commit()

def validate_and_create_table(cursor, conn):
	global table_dic
	for key, value in table_dic.items():
		table_status = check_table_exists(table_name=key, cursor=cursor)
		if table_status == "True":
			pass
		else:
			create_table(create_query=value, cursor=cursor, conn=conn)

def check_weather_data(cursor):
	global check_row_query
	check_weather_data_query = check_row_query.format("weather_data")
	cursor.execute(check_weather_data_query)
	records = cursor.fetchall()
	if not records:
		weather_data_df.to_sql('weather_data', con=conn1, if_exists='append', index=False)
	else:
		cursor.execute(check_last_entry_query)
		last_date = cursor.fetchall()[0]
		new_dates = prep_dates(last_date)
		if new_dates == []:
			pass
		else:
			client_setup()
			resp = call_api(start_date=new_dates(0), end_date=new_dates(1))
			update_weather_data_df = process_data(resp=resp)
			update_weather_data_df.to_sql('weather_data', con=conn1, if_exists='append', index=False)

# Run Application
if __name__ == "__main__":
	conn = create_post_conn()
	conn = check_post_conn(conn)
	cursor = conn.cursor()
	validate_and_create_table(cursor=cursor, conn=conn) # Arguably redundant, but helps to better format the dates
	dba_project_data_df.to_sql('project_data', con=conn1, if_exists='append', index=False) # Project data has no time stamp, so let's keep things consitant.  
	mlb_data.to_sql('mlb_data', con=conn1, if_exists='append', index=False) # I'm only doing this once.
	check_weather_data(cursor=cursor)
	conn.close() # Just good etiquite. 