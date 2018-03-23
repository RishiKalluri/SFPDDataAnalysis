import csv
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd

import numpy as np
import datetime

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

def makeAverageDispatch():

    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)



    temp = []
    zipCodes = []
    averageDispatch = []

    for element in csvFile1:
        csvFile.append(element)

    for view in csvFile:
        temp.append(view[17])

    temp = sort(temp)

    for index in temp:
        if index not in zipCodes:
            zipCodes.append(index)

    print zipCodes

    i = 0
    while(i < len(zipCodes)):

        store = []
        sum = 0

        for row in csvFile:

            dispatchYear = row[8][0:4]
            dispatchMonth = row[8][5:7]
            dispatchDate = row[8][8:10]
            dispatchHours = row[8][11:13]
            dispatchMinutes = row[8][14:16]
            dispatchSeconds = row[8][17:19]

            time1 = datetime.datetime(year = int(dispatchYear), month = int(dispatchMonth), day = int(dispatchDate), hour = int(dispatchHours), minute = int(dispatchMinutes), second = int(dispatchSeconds))

            receivedYear = row[6][0:4]
            receivedMonth = row[6][5:7]
            receivedDate = row[6][8:10]
            receivedHours = row[6][11:13]
            receivedMinutes = row[6][14:16]
            receivedSeconds = row[6][17:19]

            time2 = datetime.datetime(year = int(receivedYear), month = int(receivedMonth), day = int(receivedDate), hour = int(receivedHours), minute = int(receivedMinutes), second = int(receivedSeconds))

            diff = time1 - time2
            diff = diff.seconds



            if row[17] == zipCodes[i]:
                store.append(diff)

        for index in store:
            sum = sum + index

        average = sum / len(store)

        averageDispatch.append(average)
        i = i + 1

    file.close()

def makeLine():
    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []
    times = []
    timeCounter = []

    for row in csvFile1:
        csvFile.append(row)

    y = 0
    while (y < 24):
        times.append(y)
        y = y+1

    medicalLine = []
    fireLine = []
    alarmLine = []
    trafficLine = []
    otherLine = []

    x = 0
    while (x < len(times)):
        medicalCount = 0
        fireCount = 0
        alarmCount = 0
        trafficCount = 0
        otherCount = 0
        for row in csvFile:
            if (int(row[6][11:13]) == x) and (row[3]=='Medical Incident'):
                medicalCount = medicalCount + 1
            elif (int(row[6][11:13]) == x) and ("Fire" in row[3] ):
                fireCount = fireCount + 1
            elif (int(row[6][11:13]) == x) and (row[3]=='Alarms'):
                alarmCount = alarmCount + 1
            elif (int(row[6][11:13]) == x) and (row[3]=='Traffic Collision'):
                trafficCount = trafficCount + 1
            elif (int(row[6][11:13]) == x):
                otherCount = otherCount + 1
        medicalLine.append(medicalCount)
        fireLine.append(fireCount)
        alarmLine.append(alarmCount)
        trafficLine.append(trafficCount)
        otherLine.append(otherCount)
        x = x + 1

    plt.plot(times, medicalLine, label = 'Medical Incidents')
    plt.plot(times, fireLine, label = 'Fire')
    plt.plot(times, alarmLine, label = 'Alarms')
    plt.plot(times, trafficLine, label = 'Traffic Collisions')
    plt.plot(times, otherLine, label = 'Other')
    plt.legend()
    plt.xlabel('Time (Hours)')
    plt.ylabel('Number of Calls Received by SFPD')
    plt.show()

def likelyDispatch():

    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []
    dispatches = []

    for row in csvFile1:
        csvFile.append(row)

    for item in csvFile:
        dispatches.append(item[27])

    print dispatches


def makeHeatmap():
    latitude = []
    longitude = []

    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    for row in csvFile:

        latitude.append(row[34])
        longitude.append(row[35])

    file.close()

    for row in latitude:
        row = float(row)

    for row in longitude:
        row = float(row)

    fig, ax = plt.subplots()

    latitude = np.array(latitude).astype(np.float)
    longitude = np.array(longitude).astype(np.float)
    latitude = pd.DataFrame(latitude)
    longitude = pd.DataFrame(longitude)

    hex_ax = ax.hexbin(x = latitude, y= longitude, gridsize = 50)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Distribution of Received Calls over GPS Location')

    plt.savefig("heatplotCalls.png")
