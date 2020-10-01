from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI, basedir
from dataaccess_dailydata import *
from config import GetURIConfig
from django.shortcuts import render
import getpass
import requests

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#TODO: Remove pre check-in
# username = input("Enter your username: ")
# password = getpass.getpass("Enter your password: ")

# # Use flask_pymongo to set up mongo connection
# SQLALCHEMY_DATABASE_URI = GetURIConfig(username, password)
# # print(SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

accepted_data_points_map = [] 
accepted_data_points_map.append({"description": "Positive Increase In Number Of Cases"
                                , "name": "positiveincrease"})

accepted_data_points_map.append({"description": "New Deaths"
                                , "name": "newdeaths"})

accepted_data_points_map.append({"description": "In ICU Currently"
                                , "name": "inicucurrently"})

accepted_data_points_map.append({"description": "On Ventilator Currently"
                                , "name": "onventilatorcurrently"})

@app.route("/home")
def home():
    return index()
    
@app.route("/")
def index(request):
    index_data = {}
    index_data["most_changed"] = loadMostChangedState(engine)
    # return render_template("index.html", index_data=index_data)
    return render(request, "index.html", {"index_data": index_data})

@app.route("/Maps")
def defaultMap():
    return heatMap("positiveincrease")


@app.route("/Maps/<dataPointName>")
def heatMap(dataPointName):
    print(dataPointName)
    map_data = {}
    map_data["datapointmap"] = accepted_data_points_map

    selectedItem = next((item for item in accepted_data_points_map if item['name'] == dataPointName), None)

    map_data["datapointdescription"] = selectedItem["description"]
    map_data["datapointname"] = selectedItem["name"]
    rawRows, map_data["rows"], map_data["quantiles"] = loadLatestData(engine, dataPointName)

    # Date is in second element
    map_data["date"] =rawRows[0]['date'].strftime("%m/%d/%Y")
    print("date", map_data["date"])
    print("map_data.rows", map_data["rows"])
    return render_template("chorplethmap.html", map_data = map_data)

@app.route("/BarGraphs")
def grades():
    grade_data = {}
    return render_template("bargraph.html")

@app.route("/Dashboard1")
def dashboard1():
    return render_template("dashboard1.html")

@app.route("/Dashboard2")
def dashboard2():
    return render_template("dashboard2.html")
 
@app.route("/Dashboard3")
def dashboard3():
    return render_template("dashboard3.html")
 
@app.route("/Dashboard4")
def dashboard4():
    return render_template("dashboard4.html")
    

if __name__ == "__main__":
    app.run()


