from sqlalchemy import create_engine
from flask import Flask, jsonify
from sqlHelper import SQLHelper


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
SQLHelper = SQLHelper()

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
    
    data =SQLHelper.executeQuery(query)
    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/stations")
def station():

    data = sqlHelper.getallstations
    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/tobs")
def temperature():
  
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

    data =SQLHelper.executeQuery(query)
    return jsonify({"ok": True, "data": data})
   
@app.route("/api/v1.0/<start>")
def startDate(start):
    
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

    data =SQLHelper.executeQuery(query)
    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/<start>/<end>")
def dateRange(start, end):
   
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

    data =SQLHelper.executeQuery(query)
    return jsonify({"ok": True, "data": data})

# Run app run
if __name__ == "__main__":
    app.run(debug=True)
