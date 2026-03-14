# William Keilsohn
# March 14, 2026

#### --- I am aware that this file can be made redundant with proper re-structuring. --- ####
#### --- I'm not sure I'm going to have time to do that, so for now I have just created this file to house important functions --- ####

# Import Packages
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2 as psy
from sqlalchemy import create_engine

# Import Support Scripts
#### --- These are only for updating the weather --- ####
from Set_Up_Code.open_metro_api import daily_dataframe as weather_data_df
from Set_Up_Code.update_open_metro_data_api import *

# Load in Secrets
load_dotenv()

# Define Variables

## Weather Variables
check_row_query = "SELECT * FROM {};"
check_last_entry_query = "SELECT weather_data.date FROM weather_data ORDER BY date DESC LIMIT 1;"

## PostgreSQL Connection Related
address = os.getenv("ADDRESS") 
port = os.getenv("PORT") 
db_name = os.getenv("DB_NAME")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD") # Too spicy not to hide. 
connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(user_name, password, address, port, db_name)
engine = create_engine(connection_string)
db = create_engine(connection_string)
conn1 = db.connect()

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

def check_weather_data(cursor):
	global check_row_query
	global check_last_entry_query
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