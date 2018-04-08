###Step 4 - Climate App

#Design a Flask api using queries developed.  Use FLASK to create routes.

#################################################
# Dependencies
#################################################
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model and reflect the tables.
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to tables
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to Tony's Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Or query the min, max, and avg temp from a start date or a date range<br/>"
        f"/api/v1.0/YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
# Query for the dates and precipitation observations from the last 365 days.
def get_precipitation():
    try:
        today = dt.date.today()
        precip = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= (today - dt.timedelta(days=365))).all()
        precip_df = pd.DataFrame(precip, columns=["date","prcp"]).set_index('date')
        precip_dict = precip_df.to_dict()
        return jsonify(precip_dict)
    except:
        return("Error! Unable to retrieve Precipitation data")
    
@app.route("/api/v1.0/stations")
# Return a json list of stations from the dataset.
def get_stations():
    try:
        station = session.query(Station.name).all()
        return jsonify(station)
    except:
        return("Error! Unable to retrieve Station data")
    
@app.route("/api/v1.0/tobs")
#Return a json list of Temperature Observations (tobs) for the previous 365 days
def get_tobs():
    try:
        today = dt.date.today()
        tobs = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= (today - dt.timedelta(days=365))).all()
        tobs_df = pd.DataFrame(tobs, columns=["date","tobs"]).set_index('date')
        tobs_dict = tobs_df.to_dict()
        return jsonify(tobs_dict)
    except:
        return("Error! Unable to retrieve Temperature Observation data")
    
@app.route("/api/v1.0/<start>")
#Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start date through today (of data available).
def calc_temp_all(start):
    try:
        end = dt.date.today()
        results = session.query(Measurement.tobs)\
            .filter(Measurement.date.between(start,end)).all()
        tempmin = min(results)
        tempmax = max(results)
        tempavg = np.mean(results)
        return jsonify({"Temp Min":tempmin[0],"Temp Max":tempmax[0],"Avg Temp":tempavg})
    except:
        return("Error! Unable to calculate for the given start date")
    
@app.route("/api/v1.0/<start>/<end>")
#Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start-end range (of data available).
def calc_temp(start, end):
    try:
        results = session.query(Measurement.tobs)\
            .filter(Measurement.date.between(start,end)).all()
        tempmin = min(results)
        tempmax = max(results)
        tempavg = np.mean(results)
        return jsonify({"Temp Min":tempmin[0],"Temp Max":tempmax[0],"Avg Temp":tempavg})
    except:
        return("Error! Unable to calculate for the given date range")
    
if __name__ == "__main__":
    app.run(debug=True)