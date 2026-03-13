# William Keilsohn
# March 13, 2026

# Import Packages
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2 as psy
from sqlalchemy import create_engine

# Load in Secrets
load_dotenv()

# Define Variables

## File Management Related
current_work_dir = os.getcwd()
current_main_dir = os.path.abspath(os.path.join(current_work_dir, os.pardir))
data_dir = os.path.join(current_main_dir, "Raw_Data")

### Data Files
dba_project_data = os.path.join(data_dir, "DBA Project - Data Set.xlsx")
# game_data # TBD
# weather_data # TBD

#### Load Data Into Pandas
dba_project_data_df = pd.read_excel(dba_project_data)
# game_data # TBD
# weather_data # TBD

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

### Table Creation Queries
table_dic = {'project_data': "CREATE TABLE IF NOT EXISTS project_data (snapshot_date date, game_date date, unique_tickets_sold int, unique_page_clicks int);"}

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

# Run Application
if __name__ == "__main__":
	conn = create_post_conn()
	conn = check_post_conn(conn)
	cursor = conn.cursor()
	validate_and_create_table(cursor=cursor, conn=conn)
	dba_project_data_df.to_sql('project_data', con=conn1, if_exists='replace', index=False) # Should "append", but no new data is coming in, so this is fine. 
	conn.close() # Just good etiquite. 