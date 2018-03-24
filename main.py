import csv
import os, requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, Markup, render_template, request
import datetime
from flask_bootstrap import Bootstrap
import math

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


        file = open('sfpd_dispatch_data_subset.csv')

        csvFile1 = csv.reader(file)
        csvFile = []
        times = []
        timeCounter = []

        for view in csvFile1:
            csvFile.append(view)

        closestLat = 0
        closestLong = 0
        distanceDiff = 100

        for row in csvFile:

            trueDistance = 0
            longDiff = 0
            latDiff = 0

            latDiff = abs(float(latitude) - float(row[34]))

            longDiff = abs(float(longitude) - float(row[35]))

            trueDistance = getDistance(latDiff, longDiff)

            if distanceDiff >= trueDistance:

                closestLat = row[34]
                closestLong = row[35]
                distanceDiff = trueDistance

        storeDiff = datetime.timedelta(hours = 24)
        likelyDispatch = ''

        for row in csvFile:

            if -0.02 <= getDistance(float(latitude) - float(row[34]), float(longitude) - float(row[35])) <= 0.02 :

                compareYear = row[6][0:4]
                compareMonth = row[6][5:7]
                compareDate = row[6][8:10]
                compareHours = time[0:2]
                compareMinutes = time[3:5]
                compareSeconds = time[6:8]


                time1 = datetime.datetime(year = int(compareYear), month = int(compareMonth), day = int(compareDate), hour = int(compareHours), minute = int(compareMinutes), second = int(compareSeconds))

                receivedYear = row[6][0:4]
                receivedMonth = row[6][5:7]
                receivedDate = row[6][8:10]
                receivedHours = row[6][11:13]
                receivedMinutes = row[6][14:16]
                receivedSeconds = row[6][17:19]

                time2 = datetime.datetime(year = int(receivedYear), month = int(receivedMonth), day = int(receivedDate), hour = int(receivedHours), minute = int(receivedMinutes), second = int(receivedSeconds))

                temp = 0

                if time1 > time2:
                    temp = time1 - time2
                    print(temp)
                else:
                    temp = time2 - time1
                    print(temp)

                if storeDiff.total_seconds() > temp.total_seconds():
                    likelyDispatch = row[27]
                    print(likelyDispatch)
                    storeDiff = temp

        file.close()

        return render_template('index.html', response = 'Dispatch: ' + likelyDispatch)


if __name__ == "__main__":
    app.run(debug = True)
