from typing import Any
from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return (
        f"Hawaii Weather Station API Homepage!!!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/2016-05-14'>/api/v1.0/START_DATE</a> --- (date must be in YYYY-MM-DD format)<br/>" 
        f"<a href='/api/v1.0/2016-05-14/2017-05-14'>/api/v1.0/START_DATE/END_DATE</a> --- (date must be in YYYY-MM-DD format)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Try to retun all rows from the measurement table
    # Grouped by date and avg precipitation 

    # How to do so? Connect to the database
    conn = engine.connect()

    # Query the database into a dataframe
    query = f"""
                SELECT
                    date,
                    avg(prcp) as avg_prcp
                FROM
                    measurement
                GROUP BY
                    date 
                ORDER BY
                    date asc;  
            """ 
    df = pd.read_sql(query, con=conn)
    conn.close()

    # Return to dataframe
    data = df.to_json(orient="records") # creates JSON string
    data = json.loads(data) # turns the string back into list of dicts

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/stations")
def station():
    # Try to retun all rows from the station table

    # How to do so? Connect to the database
    conn = engine.connect()

    # Query the database into a dataframe
    query = f"""
                SELECT
                    *
                FROM
                    station
            """
    df = pd.read_sql(query, con=conn)
    conn.close()

    # Return to dataframe
    data = df.to_json(orient="records") # creates JSON string
    data = json.loads(data) # turns the string back into list of dicts

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/tobs")
def temperature():
    # Try to retun all rows from the most popular station for last year

    # How to do so? Connect to the database
    conn = engine.connect()

    # Query the database into a dataframe
    query = f"""
                SELECT
                    station,
                    date,
                    tobs as temperature
                FROM
                    measurement 
                WHERE
                    station = 'USC00519281'
                    and date >= '2016-08-23'
                ORDER BY
                    date asc;
            """
    df = pd.read_sql(query, con=conn)
    conn.close()

    # Return to dataframe
    data = df.to_json(orient="records") # creates JSON string
    data = json.loads(data) # turns the string back into list of dicts

    return jsonify({"ok": True, "data": data})
   
@app.route("/api/v1.0/<start>")
def startDate(start):
    # Try to retun all rows from the measurement table for a specific date

    # How to do so? Connect to the database
    conn = engine.connect()

    # Query the database into a dataframe
    query = f"""
                SELECT
                    date,
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                WHERE
                    date = '{start}'     
            """
    df = pd.read_sql(query, con=conn)
    conn.close()

    # Return to dataframe
    data = df.to_json(orient="records") # creates JSON string
    data = json.loads(data) # turns the string back into list of dicts

    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/<start>/<end>")
def dateRange(start, end):
    # Try to retun all rows from the meaurement table for a specific range of dates 

    # How to do so? Connect to the database
    conn = engine.connect()

    # Query the database into a dataframe
    query = f"""
                SELECT
                    min(date) as start_date,
                    max(date) as end_date,
                    min(tobs) as min_temp,
                    avg(tobs) as avg_temp,
                    max(tobs) as max_temp
                FROM
                    measurement
                WHERE
                    date >= '{start}'
                    and date <='{end}'     
            """
    df = pd.read_sql(query, con=conn)
    conn.close()

    # Return to dataframe
    data = df.to_json(orient="records") # creates JSON string
    data = json.loads(data) # turns the string back into list of dicts

    return jsonify({"ok": True, "data": data})

# Run app run
if __name__ == "__main__":
    app.run(debug=True)
