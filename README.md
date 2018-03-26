# SFPDDataAnalysis
This is my submission to the MindSumo Challenge for Capital One

# Data Analysis
All of the data analysis for this web application was done in python. The
libraries used were matplotlib, pandas, numpy, and sklearn. All of the graphing
was done by reading the .csv file into an array, then splitting the array rows
into the desired pieces based on its index. The desired graphs were then
created using these arrays through the matplotlib and pandas libraries. All
of this code can be found in getGraphs.py. Each graph creation has its own
method, which are all called in the getGraphs() method in the .py file.

A k nearest neighbor algorithm was used to predict the most likely dispatch
based on location and time. The model was trained using the latitude, longitude,
and received timestamp from sfpd_dispatch_data_subset.csv. The prediction is
based on the 3 closest neighbors to the input data point. The reason for this
is so predictions based on location away from the 94102/94103 area do not
require lots of data points that are far away. Most of the calls are centered
around 94102/94103, and reducing the number of neighbors in the prediction
increases the accuracy of other cases, while retaining the accuracy of
predictions based around the more populated data.

# Front-End
The front end of this application was handled by the Flask web framework, along
with the Bootstrap library. Flask was used because it is able to create 4
attractive, functional web designs, with a lightweight design. Additionally,
because Flask uses python, it provides a better standard library and allows
for faster development.
