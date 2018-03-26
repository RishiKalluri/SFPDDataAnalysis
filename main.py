import csv
import os, requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, Markup, render_template, request
import datetime
from flask_bootstrap import Bootstrap
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

app = Flask(__name__)
Bootstrap(app)

def sort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return sort(less)+equal+sort(greater)
    else:
        return array

def getDistance(latitude, longitude):
    distance = math.pow((math.pow(latitude,2) + math.pow(longitude, 2)),0.5)
    return distance

def replaceDistance(array, distance):

    array = sort(array)
    x = 0
    changeValue = False
    holdValue = 0
    while(x < len(array)):
        if distance > array[x]:
            changeValue = True
            holdValue = x
        else:
            break
        x = x + 1

    if changeValue:
        array[holdValue] = distance
        print array[holdValue]
        return array
    else:
        return array

def mostLikelyDispatch(lat, lon, time):
    names = ['latitude', 'longitude', "received_timestamp", 'unit_type']
    dataset = pd.read_csv('./sfpd_dispatch_data_subset_knn.csv')
    dataset = pd.DataFrame(dataset, columns = names)

    #Convert all timestamps into datetime.timedelta objects and get total_seconds
    arr = []
    count = 0
    while(count<10000):
        format = "%Y-%m-%d %H:%M:%S.%f %Z"
        t = datetime.strptime(dataset.received_timestamp.at[count], format)
        arr.append((timedelta(hours = t.hour, minutes = t.minute, seconds = t.second).total_seconds()))
        count = count +1

    #add new values for received_timestamp to dataset to be used for predictions
    dataset['received_timestamp'] = arr

    #manipulate input
    lat = float(lat)
    lon = float(lon)
    format = "%H:%M:%S"
    t = datetime.strptime(time, format)
    time = timedelta(hours = t.hour, minutes = t.minute, seconds = t.second).total_seconds()

    input = [[lat, lon, time]]

    #set values to train classifier
    xtrain = dataset.iloc[:, :-1].values
    ytrain = dataset.iloc[:, 3].values

    #Set train and test data
    #xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = 0.20)

    #Normalize Columns, so there is no "overpowering" values
    scaler = StandardScaler()
    scaler.fit(xtrain)

    xtrain = scaler.transform(xtrain)
    input = scaler.transform(input)

    classifier = KNeighborsClassifier(n_neighbors = 5)
    classifier.fit(xtrain, ytrain)
    output = classifier.predict(input)
    return output

@app.route("/")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route("/index.html", methods = ['POST'])
def likelyDispatch():

    if request.method == "POST":

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        time = request.form.get("time")

        likelyDispatch = mostLikelyDispatch(latitude, longitude, time)
        print likelyDispatch

        return render_template('index.html', response = 'Dispatch: ' + likelyDispatch)


if __name__ == "__main__":
    app.run(debug = True)
