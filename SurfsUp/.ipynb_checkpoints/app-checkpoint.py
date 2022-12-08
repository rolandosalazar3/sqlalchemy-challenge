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

#Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create the session link
    session = Session(engine)

    #Query precipitation and date values 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    #Create dictionary 
    precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
        precipitation.append(r)
        
    #jsonify list
    return jsonify(precipitation)

#Stations    
@app.route("/api/v1.0/stations")
def stations():
    #Create the session link
    session = Session(engine)
    
    #Query satation and names
    results = session.query(Station.station, Station.name).all()
    session.close()

    #Create list of dictionaries for station and name
    station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    
    #jsonify list
    return jsonify(station_list)

#Temperature
@app.route("/api/v1.0/tobs")
def tobs():
    #Create session link
    session = Session(engine)
    
    #Query tempratures from a year from the last data point. 
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= yr_date).all()
    session.close()

    #Create list of date and temprature values
    tobs_list = []
    for result in results:
        r = {}
        r["date"] = result[1]
        r["temprature"] = result[0]
        tobs_list.append(r)

    #jsonify list
    return jsonify(tobs_list)

#run the app
if __name__ == "__main__":
    app.run(debug=True)