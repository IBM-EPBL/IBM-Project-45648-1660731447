import time
import requests

import flask
from flask import request, render_template
from flask_cors import CORS
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Uduv0cM_2Z6a-R35O__XumphA0ZXA_ztzP4feuDTZcjY"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = flask.Flask(__name__, static_url_path='')
CORS(app)
@app.route('/', methods=['GET'])
def home():
    return render_template('mainpage.html')

@app.route('/prediction', methods=['POST','GET'])
def prediction():
    fnum = (request.form['fname'])
    Month = (request.form['month'])
    Dayofmonth= (request.form['daymonth'])
    Dayofweek= (request.form['dayweek'])
    origin=(request.form['origin'])
    Destination=str(request.form['destination'])
    scheduleddeparturetime=request.form['sdeparttime']
    scheduledarrivaltime=request.form['sarrivaltime']
    Actualtime=request.form['adeparttime']
    x = [[fnum,Month,Dayofmonth,Dayofweek,origin,Destination,scheduleddeparturetime,scheduledarrivaltime,Actualtime]]
    payload_scoring = {"input_data":[{"field":[['Enter flight number','Month','Day of Month','Day of week','origin','Destination','Scheduled departure time','scheduled arrival time','actual time']],"values":x}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0dcdb632-6bab-46ba-8871-7b261b996a77/predictions?version=2022-11-16', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    print("Final prediction :",predictions)
    predict = predictions['predictions'][0]['values'][0][0]
    if(predict == 0):
        ans = "The Flight will be on time"
    else:
        ans = "The Flight will be delayed"
    
    return render_template('index.html',data=ans)

if __name__ == '__main__' :
    app.run(debug= False)
