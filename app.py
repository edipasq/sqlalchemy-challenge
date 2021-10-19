from flask import Flask, jsonify
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.sql.expression import true

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation_func():
    session = Session(engine)
    MaxDate = session.query(func.max(Measurement.date)).all()
    Maxi = MaxDate[0]
    from datetime import datetime
    a=datetime.strptime(Maxi[0], '%Y-%m-%d').date()
    Yearago = a - dt.timedelta(days=365)
    Yearagostr=Yearago.strftime('%Y-%m-%d')
    YearDates = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).\
    filter(Measurement.date >= Yearagostr).all()
    session.close()
    list = []
    for date1, prep in YearDates:
        dict = {}
        dict["date"] = date1
        dict["prcp"] = prep
        list.append(dict)

    return jsonify(list)

@app.route("/api/v1.0/stations")
def station_func():
    session = Session(engine)
    results2 = session.query(Station.station).\
    order_by(Station.station.desc()).all()
    all_stations = list(np.ravel(results2))
    session.close()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs_func():
    session = Session(engine)
    MaxDate = session.query(func.max(Measurement.date)).all()
    Maxi = MaxDate[0]
    from datetime import datetime
    a=datetime.strptime(Maxi[0], '%Y-%m-%d').date()
    Yearago = a - dt.timedelta(days=365)
    Yearagostr=Yearago.strftime('%Y-%m-%d')
    Yearagostation = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= Yearagostr).filter_by(station="USC00519281").all()
    session.close()
    list2 = []
    for date2, temp in Yearagostation:
        dict2 = {}
        dict2["date"] = date2
        dict2["tobs"] = temp
        list2.append(dict2)

    return jsonify(list2)
    return("im in tobs")

@app.route("/api/v1.0/<start>")
def Search_by_date(start):
    
    year = start[0:4]
    month = start[4:6]
    day = start[6:9]

    isValidDate = True
    try:
        dt.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate):
        session = Session(engine)
        startdate = str(year) + "-" + str(month) + "-" + str(day)        
        Maxtemp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= startdate).all()
        Mintemp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= startdate).all()
        Avgtemp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).all()
        dict3 = {}
        list3 = []
        dict3["Maxtemp"] = Maxtemp[0][0]  
        dict3["Mintemp"] = Mintemp[0][0]
        dict3["Avgtemp"] = Avgtemp[0][0]
        list3.append(dict3)
        return jsonify(list3)
        session.close()
    else:
        return("not valid please use yyyymmdd")

@app.route("/api/v1.0/<start>/<end>")
def Search_by_dates(start,end):
    
    year = start[0:4]
    month = start[4:6]
    day = start[6:9]

    isValidDate = True
    try:
        dt.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    year2 = end[0:4]
    month2 = end[4:6]
    day2 = end[6:9]
    
    isValidDate2 = True
    try:
        dt.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate2 = False
    
    if (start < end) & (isValidDate) & (isValidDate2):
        startgreater = True
    else:
        startgreater = False

    if(isValidDate) & (isValidDate2) & (startgreater):
        session = Session(engine)
        startdate = str(year) + "-" + str(month) + "-" + str(day)   
        enddate = str(year2) + "-" + str(month2) + "-" + str(day2)             
        Maxtemp = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
        Mintemp = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
        Avgtemp = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
        
        dict4 = {}
        list4 = []
        dict4["Maxtemp"] = Maxtemp[0][0]  
        dict4["Mintemp"] = Mintemp[0][0]
        dict4["Avgtemp"] = Avgtemp[0][0]
        list4.append(dict4)
        return jsonify(list4)
        session.close()
    else:
        return("not valid, please use yyyymmdd and start date should be not greater than end date")

@app.route("/")
def welcome():
    return (
        f"Welcome to the Justice League API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        
    )



if __name__ == "__main__":
    app.run(debug=True)
