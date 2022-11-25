import pickle
import json
import requests
# import numpy as np
# import pandas as pd
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form.html')
def form():
    return render_template('form.html')

@app.route('/predict', methods = ['POST','GET'])
def predict():
    GRE_Score = request.form['gre']
    TOEFL_Score = request.form['toefl']
    University_Rating = request.form['Rating']
    SOP = request.form['sop']
    LOR = request.form['lor']
    CGPA = request.form['cgpa']
    Research = request.form['research']

    
    API_KEY = "vedOZgOvlWZD3dgsWqBSURg8tYjMBpPpNMTPflIevz8s"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, 
                                                    "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})

    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
	
    payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA", "Research"]], 
                                    "values": [[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0ae1bf6a-f7e8-42f7-bfc7-5117d668c659/predictions?version=2022-11-19', 
                            json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    probability = response_scoring.json()['predictions'][0]['values'][0][0][0]
    output = probability
    # final_features = pd.DataFrame([[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]])
    # final_features = final_features.to_numpy()

    output = output*100
    output = round(output,2)

    message = "Good luck!"
    if output < 60:
        message = "Better Luck Next Time"
    
    return render_template('predict.html', prediction_text = "Admission Chances:  {}% ".format(output), message = message)
    # , data = final_features)

if __name__ == '__main__':
    app.run(debug = True)