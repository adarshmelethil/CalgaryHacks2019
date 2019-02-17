import os
from flask import render_template, jsonify, make_response, request, redirect, url_for, send_from_directory

from io import StringIO
import random
import datetime
import csv
import json

from app import app
from app import mongo

@app.route('/web/create_test_data')
def createTestData():
  result = mongo.db.crimes.insert_many(gendata())
  
  # insert_id = mongo.db.users.insert_one({"user": "asdf", "other": "stuff"}).inserted_id
  return "Inserted: {}".format(len(result.inserted_ids))

@app.route('/web/get_all_crimes')
def getAllCrimes():
  return jsonify(getAllCrimesFromDB())

@app.route("/web/download_all_crimes")
def downloadAll():
  crimes = getAllCrimesFromDB()
  si = StringIO()
  cw = csv.writer(si)

  cw.writerow(["lon", "lat", "crime", "description", "time"])
  
  cw.writerows([
    [
      crime["lon"],
      crime["lat"],
      crime["crime"],
      crime["description"],
      crime["time"]
    ] for crime in crimes])
  output = make_response(si.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=crimes.csv"
  output.headers["Content-type"] = "text/csv"
  return output

@app.route("/web/submit_crime", methods=['POST'])
def newCrimeData():
  data = json.loads(request.data)
  data["lon"] = round(data["lon"], 5)
  data["lat"] = round(data["lat"], 5)
  id_ret = mongo.db.crimes.insert_one(data)
  return redirect(url_for("index"))

@app.route('/web', defaults={"path":""})
@app.route('/web/<path:path>')
def index(path):
  path_dir = os.path.abspath("builds")
  if path != "" and os.path.exists(os.path.join(path_dir, path)):
    return make_response(send_from_directory(os.path.join(path_dir), path))
  else:
    return make_response(render_template("index.html"))


def getAllCrimesFromDB():
  return [{k: c[k] for k in c if k != "_id"} for c in mongo.db.crimes.find()]
def gendata():
  lon_limits = (-114.22191, -113.91841)
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
          "lon": round(random.uniform(*lon_limits), 5),
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
