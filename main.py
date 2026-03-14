# William Keilsohn
# March 14, 2026

# Import Packages
from flask import Flask

# Start Flask
app = Flask(__name__)

# Declare Routes and functions

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"