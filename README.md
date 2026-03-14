# Cardinals_Database_Administrator_Project

This project serves as a an example to model how ticket sales may be affected by changes in weather prior to a baseball game.

## Instalation and Setup

### Installing PostgreSQL

 If you intend for this be run locally then you will need to install postgreSQL on to your machine. If you intend to use a server or cloud based system, then you can presumably skip this part, and follow the instructions provided by your host provider. 

 To install PostgreSQL navigate to the link provided at the bottom, select the download file format appropriate for your system, and follow the onscreen instructions.

 At some point in the installation / setup process, you will be asked to provide a name, port, and password for your postgreSQL instance. This project assumes that the name and port are both the default options provided by the instalation wizard. If you change these default options, you will need to change their respective values in the code. This is NOT reccomended.  

 Once you have decided on a password, please include it in the .env file. An example is provided below. 

### Configuring Your System

I used a virtual environment for this project. If you would like to do the same, then you may instantiate one using one of the following python commands:

```
python venv venv

python -m venv venv
```
Which version you need to execute is system dependent. 

Once you have created a virtual environment (and presumably activated it), you will need to install the required python packages. These can be found in the requierments.txt file and can be installed as normal:

```
pip install -r requirements.txt
```

You will also need to supply your own .env file. The following variables will need to be provided:

```
PASSWORD = "####"

ADDRESS = "127.0.0.1"
PORT = "5432"
DB_NAME = "postgres"
USER_NAME = "postgres"
```
Replace the hastag sysmbol(s) with your keys / passwords. 

Then place this file in the main project directory. Python should be able to find it on its own. 

### Loading Data

To load the data navigate to the "Set_Up_Code" folder and execute the following comands:

```
python data_loader.py
```

Assuming your .env file is configured correctly, and your PostgreSQL instance is running, this should import all of your data into the DB. If you would like to check it, PostgreSQL comes nativly with PgAdmin, which can be used to better visualize DB schemas. 

## Use

TBA

## License

A standard MIT license is in place for this project.

## Sources

PostgreSQL = https://www.postgresql.org/

Weather API = https://open-meteo.com/

MLB Data API = https://github.com/jldbc/pybaseball