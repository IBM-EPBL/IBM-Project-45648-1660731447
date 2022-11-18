from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
import os
model = pickle.load(open('flight_new.pk1','rb'))
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("mainpage.html")

@app.route('/prediction',methods=['GET','POST'])
def predict():
    name = request.form['fname'] 
    month = request.form['month'] 
    dayofmonth = request.form['daymonth'] 
    dayofweek = request.form['dayweek'] 
    origin = request.form['origin'] 
    if(origin == "msp"):
        origin1, origin2, origin3, origin4, origin5 = 0,0,0,0,1 
    if(origin == "dtw"):
        origin1, origin2, origin3, origin4, origin5 = 1,0,0,0,0 
    if(origin == "jfk"):
        origin1, origin2, origin3, origin4, origin5 = 0,0,1,0,0, 
    if(origin == "sea"):
        origin1, origin2, origin3, origin4, origin5 = 0,1,0,0,0 
    if(origin == "atl"):
        origin1, origin2, origin3, origin4, origin5 = 0,0,0,1,0
    destination = request.form['destination']
    if(destination == "msp"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,0,0,1
    if(destination == "dtw"):
        destination1,destination2,destination3,destination4,destination5 = 1,0,0,0,0
    if(destination == "jfk"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,1,0,0
    if(destination == "sea"):
        destination1,destination2,destination3,destination4,destination5 = 0,1,0,0,0
    if(destination == "atl"):
        destination1,destination2,destination3,destination4,destination5 = 0,0,0,1,0
    dept = request.form['sdeparttime']
    arrtime = request.form['sarrivaltime']
    actdept = request.form['adeparttime']
    dept15 = int(dept)-int(actdept)
    total = [[name,month,dayofmonth,dayofweek,arrtime,dept15,origin1,origin2,origin3,origin4,origin5,destination1,destination2,destination3,destination4,destination5]]
    y_pred = model.predict(total)
    print(y_pred)
    if(y_pred == [0.]):
        ans = "The Flight will be on time"
    else:
        ans = "The Flight will be delayed"
    return render_template("index.html",data = ans)

app.run(debug=True)