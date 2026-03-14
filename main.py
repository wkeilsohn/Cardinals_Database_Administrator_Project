# William Keilsohn
# March 14, 2026

# Import Packages
from flask import Flask, render_template, url_for
from markupsafe import Markup

# Import Custom Scripts
from db_conn_manager import general_query, get_all_tables, get_table_cols

# Define Global Functions
table_list = get_all_tables()
cols_dict = get_table_cols(table_list=table_list)
proj_cols = cols_dict['project_data'] # Yes, hard coding, I'm sorry...
weather_cols = cols_dict['weather_data']
mlb_cols = cols_dict['mlb_data']
table_html_vals = ""
for i in range(0, len(weather_cols)):
	try:
		proj_val = "<td>{}</td> ".format(proj_cols[i])
	except:
		proj_val = "<td></td> "
	try:
		weath_val = "<td>{}</td> ".format(weather_cols[i])
	except:
		weath_val = "<td></td> "
	try:
		mlb_val = "<td>{}</td> ".format(mlb_cols[i])
	except:
		mlb_val = "<td></td> "
	table_html_vals = table_html_vals + "<tr> " + proj_val + weath_val + mlb_val + "</tr> "
table_html_vals = Markup(table_html_vals)

# Start Flask
app = Flask(__name__)

# Declare Routes and functions

@app.route("/")
def index():
	global cols_list
	global table_html_vals
	return render_template('index.html', table_html_vals=table_html_vals, table_list=table_list)

@app.route("/builder")
def builder():
	return "<p>Query Builder Goes Here</p>"

@app.route("/about")
def about():
	return "<p>Welcome to the About Page</p>"