import os
from flask import render_template, jsonify, make_response, request, redirect, url_for, send_from_directory

from io import StringIO
import random
import datetime
import csv
import json
import spacy
from collections import Counter

from app import app
from app import mongo


nlp = spacy.load('en')

@app.route('/create_test_data')
def createTestData():
  result = mongo.db.crimes.insert_many(gendata())
  
  # insert_id = mongo.db.users.insert_one({"user": "asdf", "other": "stuff"}).inserted_id
  return "Inserted: {}".format(len(result.inserted_ids))

@app.route('/delete_all')
def deleteAllData():
  mongo.db.crimes.drop()
  return "droped crimes data"

@app.route('/get_all_crimes')
def getAllCrimes():
  return jsonify(getAllCrimesFromDB())

@app.route("/download_all_crimes")
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

@app.route("/submit_crime", methods=['POST'])
def newCrimeData():
  data = json.loads(request.data)
  data["lon"] = round(data["lon"], 5)
  data["lat"] = round(data["lat"], 5)

  nlpDescription = nlp(data["description"])

  nouns = [ token.text for token in nlpDescription if token.is_stop != True and token.is_punct !=True and token.pos_ == 'NOUN']
  verbs = [ token.text for token in nlpDescription if token.is_stop != True and token.is_punct !=True and token.pos_ == 'VERB']
  data["common_nouns"] = Counter(nouns).most_common(3)
  data["common_verbs"] = Counter(verbs).most_common(3)

  id_ret = mongo.db.crimes.insert_one(data)
  return redirect(url_for("index"))

@app.route('/', defaults={"path":""})
@app.route('/<path:path>')
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
  
  # more
  description = [
    "I got robbed. Robbed, robbed, robbed",
    "Someone robbed me. Robbed, robbed, robbed",
    "Somebody stole my car. Car,car,car,car,stole,stole,stole,stole.",
  ]

  all_data = []
  for result in perdelta(time_limit[0], time_limit[1], datetime.timedelta(hours=1)):
    # for i in range(2):
    if random.uniform(0,1) < 0.5:
      all_data.append({
        "lon": round(random.uniform(*lon_limits), 5),
        "lat": round(random.uniform(*lat_limits), 5),
        
        "crime": random.choice(crime_categories),
        "description": random.choice(description),
        "time": unix_time_millis(result)
      })

  coordinate_centers = (-114.05518, 51.03743)
  for i in range(15):
    all_data.append({
      "lon": round((random.uniform(-20, 20) * 0.00001) + coordinate_centers[0], 5),
      "lat": round((random.uniform(-20, 20) * 0.00001) + coordinate_centers[1], 5),
      
      "crime": random.choice(crime_categories),
      "description": random.choice(description),
      "time": unix_time_millis(result)
    })
    
  for data in all_data:
    addNLPData(data)

  return all_data


def addNLPData(data):
  nlpDescription = nlp(data["description"].lower())

  nouns = [ token.text for token in nlpDescription if token.is_stop != True and token.is_punct !=True and token.pos_ == 'NOUN']
  verbs = [ token.text for token in nlpDescription if token.is_stop != True and token.is_punct !=True and token.pos_ == 'VERB']
  data["common_nouns"] = [c[0] for c in Counter(nouns).most_common(3)]
  data["common_verbs"] = [c[0] for c in Counter(verbs).most_common(3)]


epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
  return (dt - epoch).total_seconds() * 1000.0

def perdelta(start, end, delta):
  curr = start
  while curr < end:
    yield curr
    curr += delta
