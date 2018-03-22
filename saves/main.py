import csv
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, Markup, render_template, url_for
app = Flask(__name__)




@app.route("/", methods = ['GET', 'POST'])
def hello():
    return render_template('main.html')


if __name__ == "__main__":
    app.run()
