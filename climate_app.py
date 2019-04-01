# Unit 10 Assignment - Surf's Up
# Step 2 - Climate App
# by Christopher Reutz

# Import numpy and datetime
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func

# Import Flask and Jsonify
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return last 12 months of precipitation data"""
    # Calculate the date 1 year ago from the last data point in the database
    lastdate = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(lastdate[0], '%Y-%m-%d').date()
    yearago = lastdate - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= yearago).\
        order_by(Measurement.date.asc()).all()
    
    # Create a dictionary from the row data and append to a list of prcp_data
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)    
    
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Perform a query to retrieve the station information
    results = session.query(Station.id, Station.station, Station.name,\
        Station.latitude, Station.longitude, Station.elevation).all()

    # Create a dictionary from the row data and append to a list of stn_data
    stn_data = []
    for id, station, name, latitude, longitude, elevation in results:
        stn_dict = {}
        stn_dict["id"] = id
        stn_dict["station"] = station
        stn_dict["name"] = name
        stn_dict["latitude"] = latitude
        stn_dict["longitude"] = longitude
        stn_dict["elevation"] = elevation
        stn_data.append(stn_dict)
    
    return jsonify(stn_data)

@app.teardown_request
def remove_session(ex=None):
    session.remove()

if __name__ == "__main__":
    app.run(debug=True)