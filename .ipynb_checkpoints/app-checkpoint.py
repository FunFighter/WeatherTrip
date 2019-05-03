import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.prcp,Measurement.date).all()
    
    date_prcp = list(np.ravel(results))

    return jsonify(date_prcp)

    all_stat = []
    for res in results:
        stat_dict = {}
        stat_dict["precipitation"] = result.prcp
        stat_dict["data"] = result.date
        all_stat.append(stat_dict)
    return jsonify(all_stat)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station,Station.name,Station.latitude, Station.longitude, Station.elevation).all()

    stat = list(np.ravel(results))

    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date,func.sum(Measurement.tobs)).\
    filter(Measurement.date >= '2016-03-05').\
    filter(Measurement.date <='2017-03-05').\
    group_by(Measurement.station,Station.name).\
    order_by(func.sum(Measurement.prcp).desc()).all()

    tob_data = list(np.ravel(results))

    return jsonify(tob_data)

@app.route("/api/v1.0/<start>")
def tob_from(start):
    

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Station.station == Measurement.station).\
    filter(Measurement.date >= start).\
    order_by(func.min(Measurement.tobs).desc()).all()
    tob_data = list(np.ravel(results))

    
    tob_data = list(np.ravel(results))

    return jsonify(tob_data)

@app.route("/api/v1.0/<start>/<end>")
def tobs_dates(start,end):
    if end != None:
        results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        order_by(func.min(Measurement.tobs).desc()).all()
        tob_data = list(np.ravel(results))

    else:
        return f'Please enter a date into the url /api/v1.0/start/end'
    
    tob_data = list(np.ravel(results))

    return jsonify(tob_data)


    
if __name__ == '__main__':
    app.run(debug=True)
