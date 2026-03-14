# William Keilsohn
# March 14, 2026

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

#### Load Data Into Pandas
dba_project_data_df = pd.read_excel(dba_project_data)