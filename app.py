# app for SQLAlchemy-Challenge
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]  (e.g. /api/v1.0/2016-09-14) <br/>"
        f"/api/v1.0/[start]/[end]  (e.g. /api/v1.0/2016-09-14/2017-06-20)"
    )

year_age = dt.date(2017, 8, 23) - dt.date(2016, 8, 23)
query_date = dt.date(2017, 8, 23) - year_age

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a 
    # dictionary using date as the key and prcp as the value.
    
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date).\
        order_by(measurement.date).all()

    # Close the session
    session.close()

    # Store results in a dictionary
    prcp_dic = dict(results)

    # Return the JSON representation of the dictionary.
    return jsonify(prcp_dic)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    # Query a list of stations from the dataset.
    result = session.query(station.name).all()
    
    # Close the session
    session.close()

    # Store results in a list
    station_list = []
    for row in result:
        station_list.append(row[0])

    # Return a JSON list of stations from the dataset.
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobos():
    
    # create variable for frequent station from jupyter notebook analysis
    frequent_station = 'USC00519281'

    # Create a session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    temp_data = session.query(measurement.tobs).filter(measurement.date >= query_date).\
        filter(measurement.station == frequent_station).\
        order_by(measurement.date).all()
    
    # Close the session
    session.close()

    # convert results to list instead of list of tuples
    temp_data_list = []
    for i in temp_data:
        temp_data_list.append(i[0])
    
    return jsonify(temp_data_list)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create a session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate TMIN, TAVG, and TMAX for 
    # all dates greater than and equal to the start date.

    # Calculate average temp
    avg_temp_query = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    avg_temp = avg_temp_query[0][0]

# Calculate highest temp
    max_temp_query = session.query(func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    max_temp = max_temp_query[0][0]

# Calculate lowest temp
    min_temp_query = session.query(func.min(measurement.tobs)).\
        filter(measurement.date >= start).all()
    min_temp = min_temp_query[0][0]

    # Close the session
    session.close()
    
    # Create list of min, avg, and max temp
    temp_list = []
    temp_list.append(min_temp)
    temp_list.append(avg_temp)
    temp_list.append(max_temp)

    # Return a JSON list of the minimum temperature, 
    # the average temperature, and the max temperature
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create a session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate TMIN, TAVG, and TMAX for 
    # all dates greater than and equal to the start date.

    # Calculate average temp
    avg_temp_query = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    avg_temp = avg_temp_query[0][0]

# Calculate highest temp
    max_temp_query = session.query(func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    max_temp = max_temp_query[0][0]

# Calculate lowest temp
    min_temp_query = session.query(func.min(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    min_temp = min_temp_query[0][0]

    # Close the session
    session.close()
    
    # Create list of min, avg, and max temp
    temp_list = []
    temp_list.append(min_temp)
    temp_list.append(avg_temp)
    temp_list.append(max_temp)

    # Return a JSON list of the minimum temperature, 
    # the average temperature, and the max temperature
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)