import csv
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import pandas as pd


def getZipCodes():

    #Reads csv file into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Creates sorted array of zip codes without repetitions
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
    return zipCodes

    file.close()

def sort(array):

    #This method follows the quicksort algorithim and sorts an array in increasing order
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

    #This method creates a graph of the average dispatch times per zip code

    #Reads csv data file into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)
    for element in csvFile1:
        csvFile.append(element)

    #Creates a sorted array containing the zip codes in the dataset, without repetition
    zipCodes = getZipCodes()

    #Initialize array to hold the average dispatch times per array, with
    #corresponding indices
    averageDispatch = []

    #Iterate through zip codes to calculate average dispatch time
    i = 0
    while(i < len(zipCodes)):

        #len(store) serves as a counter to divide by when calculating the average
        store = []
        sum = 0

        for row in csvFile:

            #corresponding indicies to datetime object parameters
            dispatchYear = row[8][0:4]
            dispatchMonth = row[8][5:7]
            dispatchDate = row[8][8:10]
            dispatchHours = row[8][11:13]
            dispatchMinutes = row[8][14:16]
            dispatchSeconds = row[8][17:19]

            #make datetime object for dispatch timestamp
            time1 = datetime.datetime(year = int(dispatchYear), month = int(dispatchMonth), day = int(dispatchDate), hour = int(dispatchHours), minute = int(dispatchMinutes), second = int(dispatchSeconds))

            #corresponding indicies to datetime object parameters
            receivedYear = row[6][0:4]
            receivedMonth = row[6][5:7]
            receivedDate = row[6][8:10]
            receivedHours = row[6][11:13]
            receivedMinutes = row[6][14:16]
            receivedSeconds = row[6][17:19]

            #make datetime object for received timestamp
            time2 = datetime.datetime(year = int(receivedYear), month = int(receivedMonth), day = int(receivedDate), hour = int(receivedHours), minute = int(receivedMinutes), second = int(receivedSeconds))

            #calulate difference between time (results in datetime.timedelta object)
            diff = time1 - time2

            #converts time difference to seconds
            diff = diff.total_seconds()

            #check if zip code is the same as the current iteration, to ensure indices corresond
            if row[17] == zipCodes[i]:
                store.append(diff)

        #computes average dispatch time
        for index in store:
            sum = sum + index
        average = sum / len(store)

        #dipatch average is added to correspond with the zip code of the same index
        averageDispatch.append(average)

        #increment counter
        i = i + 1

    file.close()

    #graph average dispatch time per zip code and save figure as "barGraph1.png"
    arangedZipCodes = np.arange(len(zipCodes))
    ccmap = ["#ff12ff", "#ff31e2" , "#ff50c5",
        "#ff6fa8","#ff8d8b","#ffac6e","#ffcb51","#ffd647","#ffcd50",
        "#ffc458","#ffba61","#ffb16a","#ffa873","#ff9e7c","#eb9369",
        "#d78856","#c27d43","#ae7230","#9a671d","#865b0a","#725907",
        "#5f5f15","#4c6523","#396b32","#267240", "#13784e", "#007e5c"]
    fig2 = plt.figure()
    plt.barh(arangedZipCodes, averageDispatch, align = 'center', color = ccmap)
    plt.xlabel('Time from Received Timestamp to Dispatch Timestamp', fontsize = 5)
    plt.ylabel('Zip Codes', fontsize = 5)
    plt.yticks(arangedZipCodes, zipCodes, fontsize = 5, rotation = 30)
    plt.title('Average Time to Dispatch per Zip Code')
    fig2.savefig('barGraph1.png')

def makeHeatmap():

    #This method creates a heatmap showing the distribution of calls over GPS location

    #Reads csv file into usable row
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)
    file.close()

    #Reads latitude and longitude into respective arrays for use in graphs and analysis
    latitude = []
    longitude = []
    for row in csvFile:
        latitude.append(float(row[34]))
        longitude.append(float(row[35]))

    #Plots data into hexbin plot using histogram style graphing, where occurances
    #are binned together over a certain region
    fig, ax = plt.subplots()
    latitude = np.array(latitude).astype(np.float)
    longitude = np.array(longitude).astype(np.float)
    latitude = pd.DataFrame(latitude)
    longitude = pd.DataFrame(longitude)
    hex_ax = ax.hexbin(x = longitude, y= latitude, gridsize = 50)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Distribution of Received Calls over GPS Location')
    plt.savefig("heatplotCalls2.png")

def fourTypes():

    #This method creates a scatter plot showing the Distribution of the different call
    #types over GPS location

    #Reads csv file into usable row
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Initialize arrays for longitude(x) and latitude(y) data for each call type
    potentialx = [] #Potentially Life-Threatening
    potentialy = []
    alarmx = [] #Alarm
    alarmy = []
    nonx = [] #Non Life-Threatening
    nony = []
    firex = [] #Fire
    firey = []

    #Iterates through csv file and adds data points to appropriate call type array
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

    #Plots four scatter plots over each other to show distribution of each call type
    figure4 = plt.figure()
    ax1 = figure4.add_subplot(111)
    ax1.scatter(potentialx, potentialy, color = '#3FB485', marker = '.', label = 'Potential Life-Threatening' )#, potential[0])
    ax1.scatter(alarmx, alarmy, color = '#ff2400', marker = '.', label = 'Alarm')
    ax1.scatter(nonx, nony, color = '#990099', marker = '.', label = 'Non Life-Threatening')
    ax1.scatter(firex, firey, color = '#4d94ff', marker = '.', label = 'Fire')
    plt.title('Distribution of Call Types over GPS Location')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid()
    figure4.savefig('fourTypes3.png')

def safestAreas():

    #This method creates a three dimensional scatter plot to show the how dangerou
    #different zip codes are based on the number of calls and their associated data
    #Levels

    #Reads csv file into usable row
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)
    for element in csvFile1:
        csvFile.append(element)

    #Creates a sorted array of zip codes without repetitions
    zipCodes = getZipCodes()

    #Calculates number of call received per zip code
    occurances = []
    for row in zipCodes:
        count = 0
        for item in csvFile:
            if int(item[17]) == row:
                count = count + 1
        occurances.append(count)

    #Calculates associated danger levels per zip codes, values correspond to the labels
    #as shown beneath
    danger = []
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

    #Scales down values for easier intereptation in graph, scale is labeled on graph
    temp=[]
    for item in zipCodes:
        temp.append(item - 94000)
    zipCodes = temp
    temp = []
    for item in occurances:
        temp.append(item/100)
    occurances = temp

    #Plots data according to number of calls and assoicated danger levels
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(zipCodes, occurances, danger, c = "#A004F2", marker = 'o')
    ax.set_xlabel('Zip Codes (94###)')
    ax.set_ylabel('Number of Calls (x100)')
    ax.set_zlabel('Associated Danger Levels')
    ax.set_title('Danger Levels and Number of Calls per Zip Code')
    fig.savefig('safestAreas1.png')

def getDayArray(zipCode):

    #This method counts the number of calls per day of input zipCode and returns an array
    #of values corresponding to the indicies of the days array below

    #Reads csv into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Counts the number of calls per day of the input zipCode and adds them to array
    array = []
    days = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    for row in days:
        count = 0
        for item in csvFile:
            if (int(item[4][8:10])==row) and (item[17]==zipCode) :
                count = count + 1
        array.append(count)

    file.close()

    return array

def dayTrend():

    #This method shows the distribution of calls per day for each zip code

    #Reads csv into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Creates sorted array of zip codes, without repetitions
    zipCodes = getZipCodes()

    #Creates array to be used for labeling x values on graph
    days = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    file.close()

    #Plots all the distributions for the zip codes in the same line graph
    fig = plt.figure()
    fig, ax = plt.subplots()
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
    plt.legend(loc='upper right', prop={'size': 5.5})
    plt.xlabel('Day (January ##, 2018)')
    plt.ylabel('Number of Calls')
    plt.title('Total Number of Calls per Day Over 12 Days')
    ax.set_xticks(days)
    fig.savefig('dayTrend3.png')

def getHourArray(zipCode):

    #This method calcutates the number of hourly calls correspond to the input zipCode
    #and returns an array with the values corresponding to the indicies of the hours array
    #below

    #Reads csv file into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Counts number of calls per hour of the input zipCode and adds them to array
    array = []
    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for row in hours:
        count = 0
        for item in csvFile:
            if (int(item[6][11:13])==row) and (item[17]==zipCode) :
                count = count + 1
        count = count
        array.append(count)

    file.close()

    return array

def hourTrend():

    #This method shows the distribution of hourly calls per zip code

    #Reads csv into usable array
    file = open('sfpd_dispatch_data_subset.csv')
    csvFile1 = csv.reader(file)
    csvFile = []
    for row in csvFile1:
        csvFile.append(row)

    #Creates a sorted array of zip codes withou repetitions
    zipCodes = getZipCodes()

    #Used to graph x axis values
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    file.close()

    #Plots all the distributions for the zip codes in the same line graph
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

    #Used to label x axis values
    hours = [0,2,4,6,8,10,12,14,16, 18,20,22]

    plt.legend(loc='upper right', prop={'size': 5.5})
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Calls')
    ax.set_xticks(hours)
    plt.title('Total Number of Calls per Hour Over 12 Days')
    figure.savefig('totalCalls1.png')

def getGraphs():

    #This method calls the methods to create and save all the graphs used for
    #data analysis in this application
    makeAverageDispatch()
    hourTrend()
    dayTrend()
    makeHeatmap()
    fourTypes()
    safestAreas()

#Calls method to get all graphs that are used in the webapp
getGraphs()
