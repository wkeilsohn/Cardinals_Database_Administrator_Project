# William Keilsohn
# March 14, 2026

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