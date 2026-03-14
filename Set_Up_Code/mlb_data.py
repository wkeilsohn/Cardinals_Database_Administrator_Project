# William Keilsohn
# March 14, 2026

# Import Packages
import pybaseball

# Define Variables
team_code = 'STL'

### For some reason, 2026 data is unavialable. 
### Also, the second half of the year has errors in it (and since the other two data sets cut off before june), I'm only including the first half of the year.
mlb_data = pybaseball.statcast(start_dt="2025-01-01", end_dt="2025-06-30", team=team_code)

## Manipulate Data
mlb_data = mlb_data[['game_date']] # We only need a schudle so this should hypothetically be fine
mlb_data = mlb_data['game_date'].str.replace('2025', '2026') # Simulating a future schedule as 2026 is not available from the API
mlb_data = mlb_data.drop_duplicates() # I'm guessing the team only plays one game per day (max).