#Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Setup Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect an existing database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link
session = Session(engine)

#Last date in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

#Calculate the date 1 year ago from the last data point in the database
yr_date = dt.date(2017,8,23) - dt.timedelta(days=365)

session.close()

#Flask
app = Flask(__name__)

#Routes
@app.route("/")
def welcome():
    """All available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of all Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
    )

