
from flask import render_template, jsonify, make_response

from io import StringIO
import random
import datetime
import csv

from app import app
from app import mongo


@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html", user={"username": "Bob"})

@app.route('/create_test_data')
def createTestData():
  result = mongo.db.crimes.insert_many(gendata())
  
  # insert_id = mongo.db.users.insert_one({"user": "asdf", "other": "stuff"}).inserted_id
  return "Inserted: {}".format(len(result.inserted_ids))

@app.route('/get_all_crimes')
def getAllCrimes():
  return jsonify(getAllCrimesFromDB())

@app.route("/download_all_crimes")
def downloadAll():
  crimes = getAllCrimesFromDB()
  si = StringIO()
  cw = csv.writer(si)

  cw.writerow(["log", "lat", "crime", "description", "time"])
  
  cw.writerows([
    [
      crime["log"],
      crime["lat"],
      crime["crime"],
      crime["description"],
      crime["time"]
    ] for crime in crimes])
  output = make_response(si.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=crimes.csv"
  output.headers["Content-type"] = "text/csv"
  return output

@app.route("/submit_crime")
def newCrimeData():
  return "NotImplemented"

def getAllCrimesFromDB():
  return [{k: c[k] for k in c if k != "_id"} for c in mongo.db.crimes.find()]
def gendata():
  log_limits = (-114.22191, -113.91841)
  lat_limits = (50.86999, 51.18267)

  crime_categories = [
    "Breaking & Entering/Robbery",
    "Violence",
    "Physical Disorder",
    "Theft FROM Vehicle",
    "Illegal Drug Activity"
  ]

  # past week
  time_limit = (datetime.datetime.today() - datetime.timedelta(days=7), datetime.datetime.today())
  
  all_data = []
  for result in perdelta(time_limit[0], time_limit[1], datetime.timedelta(hours=1)):
    for i in range(2):
      if random.uniform(0,1) < 0.5:
        all_data.append({
          "log": round(random.uniform(*log_limits), 5),
          "lat": round(random.uniform(*lat_limits), 5),
          
          "crime": random.choice(crime_categories),
          "description": "",
          "time": unix_time_millis(result)
        })
  return all_data

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
  return (dt - epoch).total_seconds() * 1000.0

def perdelta(start, end, delta):
  curr = start
  while curr < end:
    yield curr
    curr += delta

{
  "crime": "Violence", 
  "description": "", 
  "lat": 50.96902, 
  "log": -113.99686, 
  "time": 1549746875898.268
}