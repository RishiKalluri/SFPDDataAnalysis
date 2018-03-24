import csv
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
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

    arangedZipCodes = np.arange(len(zipCodes))

    plt.barh(arangedZipCodes, averageDispatch, align = 'center')
    plt.show()

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
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.title('Distribution of Received Calls over GPS Location')

    plt.savefig("heatplotCalls.png")

def getItems(array, index):
    new = []
    for item in array:
        new.append(item[index])
    return new

def fourTypes():
    data_frame = pd.read_csv('./sfpd_dispatch_data_subset.csv')

    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)


    potentialx = []
    potentialy = []
    alarmx = []
    alarmy = []
    nonx = []
    nony = []
    firex = []
    firey = []

    for row in csvFile:

        if row[25] == 'Potentially Life-Threatening':
            potentialx.append(float(row[35]))
            potentialy.append(float(row[34]))
        elif row[25] == 'Alarm':
            alarmx.append(float(row[35]))
            alarmy.append(float(row[34]))
        elif row[25] == 'Non Life-threatening':
            nonx.append(float(row[35]))
            nony.append(float(row[34]))
        else:
            firex.append(float(row[35]))
            firey.append(float(row[34]))

    figure4 = plt.figure()
    ax1 = figure4.add_subplot(111)
    ax1.scatter(potentialx, potentialy, color = '#3FB485', marker = '.', label = 'Potential Life-Threatening' )#, potential[0])
    ax1.scatter(alarmx, alarmy, color = '#800000', marker = '.', label = 'Alarm')
    ax1.scatter(nonx, nony, color = '#990099', marker = '.', label = 'Non Life-Threatening')
    ax1.scatter(firex, firey, color = '#4d94ff', marker = '.', label = 'Fire')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    figure4.savefig('fourTypes.png')

def safestAreas():
    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    temp = []
    zipCodes = []
    occurances = []
    danger = []

    for element in csvFile1:
        csvFile.append(element)

    for view in csvFile:
        temp.append(int(view[17]))

    temp = sort(temp)

    for index in temp:
        if index not in zipCodes:
            zipCodes.append(index)

    zipCodes = sort(zipCodes)

    print zipCodes

    for row in zipCodes:

        count = 0

        for item in csvFile:
            if int(item[17]) == row:
                count = count + 1

        occurances.append(count)

    print occurances

    for item in zipCodes:

        count = 0

        for row in csvFile:
            if int(row[17]) == item:

                if row[25] == 'Potentially Life-Threatening':
                    count = count + 5
                elif row[25] == 'Fire':
                    count = count + 3
                elif row[25] == 'Non Life-threatening':
                    count = count + 2
                else:
                    count = count + 1

        danger.append(count)

    print danger

    temp1 = []

    for item in zipCodes:
        temp1.append(item - 94000)

    zipCodes = temp1

    temp = []

    for item in occurances:
        temp.append(item/100)

    occurances = temp


    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(zipCodes, occurances, danger, c = "#A004F2", marker = 'o')
    ax.set_xlabel('Zip Codes (94###)')
    ax.set_ylabel('Number of Calls (x100)')
    ax.set_zlabel('Danger Level Associated with Area')
    ax.set_title('Danger Levels and Number of Calls per Zip Code')
    plt.show()

def getDayArray(zipCode):
    file = open('sfpd_dispatch_data_subset.csv')

    array = []

    days = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    for row in days:
        count = 0
        for item in csvFile:
            if (int(item[4][8:10])==row) and (item[17]==zipCode) :
                count = count + 1
        array.append(count)

    file.close()

    return array

def dayTrend():
    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    temp = []
    zipCodes = []

    for element in csvFile1:
        csvFile.append(element)

    for view in csvFile:
        temp.append(view[17])

    temp = sort(temp)

    for index in temp:
        if index not in zipCodes:
            zipCodes.append(index)

    days = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    file.close()

    figure = plt.figure()
    plt.plot(days, getDayArray(zipCodes[0]), label = zipCodes[0])
    plt.plot(days, getDayArray(zipCodes[1]), label = zipCodes[1])
    plt.plot(days, getDayArray(zipCodes[2]), label = zipCodes[2])
    plt.plot(days, getDayArray(zipCodes[3]), label = zipCodes[3])
    plt.plot(days, getDayArray(zipCodes[4]), label = zipCodes[4])
    plt.plot(days, getDayArray(zipCodes[5]), label = zipCodes[5])
    plt.plot(days, getDayArray(zipCodes[6]), label = zipCodes[6])
    plt.plot(days, getDayArray(zipCodes[7]), label = zipCodes[7])
    plt.plot(days, getDayArray(zipCodes[8]), label = zipCodes[8])
    plt.plot(days, getDayArray(zipCodes[9]), label = zipCodes[9])
    plt.plot(days, getDayArray(zipCodes[10]), label = zipCodes[10])
    plt.plot(days, getDayArray(zipCodes[11]), label = zipCodes[11])
    plt.plot(days, getDayArray(zipCodes[12]), label = zipCodes[12])
    plt.plot(days, getDayArray(zipCodes[13]), label = zipCodes[13])
    plt.plot(days, getDayArray(zipCodes[14]), label = zipCodes[14])
    plt.plot(days, getDayArray(zipCodes[15]), label = zipCodes[15])
    plt.plot(days, getDayArray(zipCodes[16]), label = zipCodes[16])
    plt.plot(days, getDayArray(zipCodes[17]), label = zipCodes[17])
    plt.plot(days, getDayArray(zipCodes[18]), label = zipCodes[18])
    plt.plot(days, getDayArray(zipCodes[19]), label = zipCodes[19])
    plt.plot(days, getDayArray(zipCodes[20]), label = zipCodes[20])
    plt.plot(days, getDayArray(zipCodes[21]), label = zipCodes[21])
    plt.plot(days, getDayArray(zipCodes[22]), label = zipCodes[22])
    plt.plot(days, getDayArray(zipCodes[23]), label = zipCodes[23])
    plt.plot(days, getDayArray(zipCodes[24]), label = zipCodes[24])
    plt.plot(days, getDayArray(zipCodes[25]), label = zipCodes[25])
    plt.plot(days, getDayArray(zipCodes[26]), label = zipCodes[26])
    plt.legend(loc='upper right')
    plt.xlabel('Day (January ##, 2018)')
    plt.ylabel('Number of Calls')
    fig.savefig('dayTrend.png')

def getHourArray(zipCode):
    file = open('sfpd_dispatch_data_subset.csv')

    array = []

    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    for row in hours:
        count = 0
        for item in csvFile:
            if (int(item[6][11:13])==row) and (item[17]==zipCode) :
                count = count + 1
        count = count
        array.append(count)

    file.close()

    return array


def makeLines():
    file = open('sfpd_dispatch_data_subset.csv')

    csvFile1 = csv.reader(file)
    csvFile = []

    for row in csvFile1:
        csvFile.append(row)

    temp = []
    zipCodes = []

    for element in csvFile1:
        csvFile.append(element)

    for view in csvFile:
        temp.append(view[17])

    temp = sort(temp)

    for index in temp:
        if index not in zipCodes:
            zipCodes.append(index)

    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    file.close()

    figure = plt.figure()
    figure, ax = plt.subplots()
    plt.plot(hours, getHourArray(zipCodes[0]), label = zipCodes[0])
    plt.plot(hours, getHourArray(zipCodes[1]), label = zipCodes[1])
    plt.plot(hours, getHourArray(zipCodes[2]), label = zipCodes[2])
    plt.plot(hours, getHourArray(zipCodes[3]), label = zipCodes[3])
    plt.plot(hours, getHourArray(zipCodes[4]), label = zipCodes[4])
    plt.plot(hours, getHourArray(zipCodes[5]), label = zipCodes[5])
    plt.plot(hours, getHourArray(zipCodes[6]), label = zipCodes[6])
    plt.plot(hours, getHourArray(zipCodes[7]), label = zipCodes[7])
    plt.plot(hours, getHourArray(zipCodes[8]), label = zipCodes[8])
    plt.plot(hours, getHourArray(zipCodes[9]), label = zipCodes[9])
    plt.plot(hours, getHourArray(zipCodes[10]), label = zipCodes[10])
    plt.plot(hours, getHourArray(zipCodes[11]), label = zipCodes[11])
    plt.plot(hours, getHourArray(zipCodes[12]), label = zipCodes[12])
    plt.plot(hours, getHourArray(zipCodes[13]), label = zipCodes[13])
    plt.plot(hours, getHourArray(zipCodes[14]), label = zipCodes[14])
    plt.plot(hours, getHourArray(zipCodes[15]), label = zipCodes[15])
    plt.plot(hours, getHourArray(zipCodes[16]), label = zipCodes[16])
    plt.plot(hours, getHourArray(zipCodes[17]), label = zipCodes[17])
    plt.plot(hours, getHourArray(zipCodes[18]), label = zipCodes[18])
    plt.plot(hours, getHourArray(zipCodes[19]), label = zipCodes[19])
    plt.plot(hours, getHourArray(zipCodes[20]), label = zipCodes[20])
    plt.plot(hours, getHourArray(zipCodes[21]), label = zipCodes[21])
    plt.plot(hours, getHourArray(zipCodes[22]), label = zipCodes[22])
    plt.plot(hours, getHourArray(zipCodes[23]), label = zipCodes[23])
    plt.plot(hours, getHourArray(zipCodes[24]), label = zipCodes[24])
    plt.plot(hours, getHourArray(zipCodes[25]), label = zipCodes[25])
    plt.plot(hours, getHourArray(zipCodes[26]), label = zipCodes[26])

    hours = [0,2,4,6,8,10,12,14,16, 18,20,22]

    plt.legend(loc='upper right', prop={'size': 5.5})
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Calls')
    ax.set_xticks(hours)
    plt.title('Average Number of Calls in 24 Hour Period')
    plt.show()

makeLines()
