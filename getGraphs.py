import csv
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt




def makePie():

    callType = []
    medicalIncident = 0
    alarms = 0
    fire = 0
    structureFire = 0
    vehicleFire = 0
    outsideFire = 0
    trafficCollision = 0
    citizenAssist = 0
    other = 0

    file = open('sfpd_dispatch_data_subset.csv')

    csvFile = csv.reader(file)

    for row in csvFile:
        callType.append(row[3])

    x = 0
    while (x < len(callType)):
        if callType[x] == 'Medical Incident':
            medicalIncident = medicalIncident + 1
        elif callType[x] == 'Alarms':
            alarms = alarms + 1
        elif callType[x] == 'Structure Fire':
            structureFire = structureFire + 1
            fire = fire + 1
        elif callType[x] == 'Vehicle Fire':
            vehicleFire = vehicleFire + 1
            fire = fire + 1
        elif callType[x] == 'Outside Fire':
            outsideFire = outsideFire + 1
            fire = fire + 1
        elif callType[x] == 'Traffic Collision':
            trafficCollision = trafficCollision + 1
        else:
            other = other + 1
        x = x + 1


    file.close()

    # Plotting Data in Pie Chart
    labels = 'Medical Incident', 'Alarms', 'Fire', 'Traffic Collision', 'Other'
    sizes = [medicalIncident, alarms, fire, trafficCollision, other]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lavender', 'turquoise']
    explode = (0.1, 0, 0, 0, 0)
    fig1 = plt.figure()
    plt.pie(sizes, explode = explode, labels = labels, colors = colors,  autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Distribution of Types of Calls')
    plt.axis('equal')
    plt.savefig('pieChart.png')

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
            diff = diff.total_seconds()

            if row[17] == zipCodes[i]:
                store.append(diff)

        print store
        break;

        for index in store:
            sum = sum + index

        average = sum / len(store)

        averageDispatch.append(average)
        i = i + 1

    file.close()

    #Plotting data in Bar Graph

    arangedZipCodes = np.arange(len(zipCodes))
    arangedAverageDispatch = np.arange(len(averageDispatch))


    fig2 = plt.figure()
    plt.barh(arangedZipCodes, averageDispatch, align = 'center', alpha = 0.5)
    plt.xlabel('Time from Received Timestamp to Dispatch Timestamp', fontsize = 5)
    plt.ylabel('Zip Codes', fontsize = 5)
    plt.yticks(arangedZipCodes, zipCodes, fontsize = 5, rotation = 30)
    plt.title('Average Time to Dispatch per Zip Code')
    fig2.savefig('barGraph.png') #('barGraph.png')

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

    file.close()

    figure3 = plt.figure()
    plt.plot(times, medicalLine, label = 'Medical Incidents')
    plt.plot(times, fireLine, label = 'Fire')
    plt.plot(times, alarmLine, label = 'Alarms')
    plt.plot(times, trafficLine, label = 'Traffic Collisions')
    plt.plot(times, otherLine, label = 'Other')
    plt.legend()
    plt.xlabel('Time (Hours)')
    plt.ylabel('Number of Calls Received by SFPD')
    figure3.savefig('lineGraph.png')

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

def getGraphs():
    makePie()
    makeAverageDispatch()
    makeLine()
    makeHeatmap()

getGraphs()
