# William Keilsohn
# March 13, 2026

# Import Packages
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2 as psy

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
port = "5432"
db_name = "postgres"
user_name = "postgres"
password = os.getenv("PASSWORD") # Too spicy not to hide. 

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
		print("Connection is Open")
		return conn
	else:
		return create_post_conn()

# Run Application
if __name__ == "__main__":
	conn = create_post_conn()
	conn = check_post_conn(conn)


	conn.close() # Just good etiquite. 