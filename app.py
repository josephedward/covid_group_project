from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from scripts import load_global

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/covid_app"
mongo = PyMongo(app)

import os
is_prod = os.environ.get('IS_HEROKU', None)
if(is_prod):
    app.config["MONGO_URI"] = os.environ.get('MONGO_URI', None)   


@app.route("/set_global_deaths_dict/", methods=['GET'])
def data_to_mongo():
    global_deaths= mongo.db.global_deaths
    data_df = load_global.global_death_df()
    global_deaths.insert_many(data_df.to_dict("records"));

@app.route("/get_global_deaths_json/", methods=['GET'])
def json_data_from_mongo():
    # ASSUMING THAT THE DATA HAS ALREADY BEEN LOADED INTO MONGO
    global_deaths= mongo.db.global_deaths
    global_data = global_deaths.find({})
    global_data= pd.DataFrame([str(x) for x in global_data])    
    return global_data.to_json()

@app.route("/get_global_deaths_csv/", methods=['GET'])
def csv_data_from_mongo():
    # ASSUMING THAT THE DATA HAS ALREADY BEEN LOADED INTO MONGO
    global_deaths= mongo.db.global_deaths
    global_data = global_deaths.find({})
    global_data= pd.DataFrame([str(x) for x in global_data])    
    return global_data.to_csv(index=False)

@app.route("/get_global_deaths_display/", methods=['GET'])
def data_html():
    global_deaths= mongo.db.global_deaths
    global_data = global_deaths.find({})
    global_data= pd.DataFrame([str(x) for x in global_data])    
    return global_data.to_html();


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Covid-19 Dashboard in Dev</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
