import csv
import os, requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, Markup, render_template, request
import datetime
from flask_bootstrap import Bootstrap

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
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array




@app.route("/")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route("/index.html", methods = ['POST'])
def likelyDispatch():

    if request.method == "POST":

        zipCode = request.form.get("zipCode")
        time = request.form.get("time")


        file = open('sfpd_dispatch_data_subset.csv')

        csvFile1 = csv.reader(file)
        csvFile = []
        times = []
        timeCounter = []

        for view in csvFile1:
            csvFile.append(view)


        temp = []
        zipCodes = []

        for view in csvFile:
            temp.append(view[17])

        temp = sort(temp)

        for index in temp:
            if index not in zipCodes:
                zipCodes.append(index)

        closestZip = 0
        zipDiff = 500000
        zipIndex = 0

        for row in zipCodes:

            tempDiff = 0

            if int(zipCode) > int(row):
                tempDiff = int(zipCode) - int(row)
            else:
                tempDiff = int(row) - int(zipCode)

            if zipDiff > tempDiff:
                closestZip = row
                zipDiff = tempDiff


        storeDiff = datetime.timedelta(hours = 2)
        likelyDispatch = ''

        for row in csvFile:

            if row[17]==closestZip:

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
                else:
                    temp = time2 - time1

                if storeDiff.total_seconds() > temp.total_seconds():
                    likelyDispatch = row[27]
                    storeDiff = temp

        file.close()
        return render_template('index.html', response = likelyDispatch)


if __name__ == "__main__":
    app.run(debug = True)
