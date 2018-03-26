from flask import Flask,  render_template, request
import datetime
from flask_bootstrap import Bootstrap
import pandas as pd
from datetime import timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
Bootstrap(app)

def mostLikelyDispatch(lat, lon, time):

    #This method uses the K nearest neighbour model to predic the most likely dispatch Type
    #based on the GPS coordintes and the time given

    #creates dataset with desired fields
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

    #Initialize classifier and train model with normalized dataset
    classifier = KNeighborsClassifier(n_neighbors = 3)
    classifier.fit(xtrain, ytrain)

    #Input and return prediction
    output = classifier.predict(input)
    return output

@app.route("/")

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route("/index.html", methods = ['POST'])
def likelyDispatch():

    #Makes sure that method is only called when form data is submitted as a POST request
    if request.method == "POST":

        #Retrieve data from submitted form
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        time = request.form.get("time")

        #Ensure data is within given GPS coordinates
        if (37.70 <= float(latitude) <= 37.84) and (-122.52 <= float(longitude) <= -122.36):

            try:

                #Uses K Nearest Neighbour to predict most likely dispatch type
                likelyDispatch = mostLikelyDispatch(latitude, longitude, time)
                return render_template('index.html', response = 'Dispatch: ' + likelyDispatch)

            except Exception as exception:

                #In case time is inputted in a wrong format, or other error occurs

                return render_template('index.html', response =  str(exception))

        else:

            #Print error message if Coordinates are out of range
            return render_template('index.html', response = 'Enter GPS Coordinates between (37.70, -122.52) and (37.84, -122.36)')

if __name__ == "__main__":
    app.run(debug = True)
