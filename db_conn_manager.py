# William Keilsohn
# March 14, 2026

# Import Packages
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import psycopg2 as psy
from sqlalchemy import create_engine

# Load Custom Scripts
from recycle_functions import create_post_conn, check_post_conn

# Load in Secrets
load_dotenv()

# Define Variables

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

conn = create_post_conn()

# Define Functions
def general_query(string):
	global engine
	try:
		df = pd.read_sql(string, con=engine)
		return df
	except:
		return pd.DataFrame() # Creates a blank on the page so and skips creating the error... hopefully...
	# global conn
	# conn = check_post_conn(conn)
	# cursor = conn.cursor()
	# try:
	# 	cursor.execute(string)
	# 	return cursor.fetchall()
	# except:
	# 	pass

def get_all_tables():
	global conn
	conn = check_post_conn(conn)
	cursor = conn.cursor()
	full_query = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');"
	cursor.execute(full_query)
	results = cursor.fetchall()
	results = [x[0] for x in results] # Tuples...
	return results

def get_table_cols(table_list):
	global conn
	conn = check_post_conn(conn)
	cursor = conn.cursor()
	column_dict = {}
	column_query = "SELECT column_name FROM information_schema.columns WHERE table_name = '{}' ORDER BY ordinal_position;"
	for i in table_list:
		cursor.execute(column_query.format(i))
		columns = [x[0] for x in cursor.fetchall()]
		column_dict[i] = columns
	return column_dict

# #### For Testing Purposes Only ####
# if __name__ == '__main__':
# 	table_list = get_all_tables()
# 	print(get_table_cols(table_list=table_list))