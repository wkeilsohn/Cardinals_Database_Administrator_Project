# William Keilsohn
# March 13, 2026

# Import Packages
import numpy as np
import pandas as pd
import os

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
address = "127.0.0.1"
port = "5432"

# Declare Functions

# Run Application
if __name__ == "__main__":
	print(dba_project_data_df)