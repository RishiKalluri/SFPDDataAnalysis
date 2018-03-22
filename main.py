import csv
import os, requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, Markup, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def likelyDispatch():
    if request.method == "POST":
        zipCode = request.form.get("Zip Code")
        print zipCode
        return render_template('index.html', zipCode = zipCode)


if __name__ == "__main__":
    app.run(debug = True)
