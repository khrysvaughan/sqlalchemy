# 1. Necessary Imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/about<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    list_stations = list(np.ravel(stations))
    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Determine a year later from that date and put date back together
    lastdatesplit = lastdate[0].split("-")
    lastdatesplit[0] = str(int(lastdatesplit[0]) - 1)
    yearlaterdate = "-".join(lastdatesplit)

    # Get all measurements from yearlaterdate onwards
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= yearlaterdate).all()
    list_tobs = list(np.ravel(tobs))
    return jsonify(list_tobs)


if __name__ == "__main__":
    app.run(debug=True)