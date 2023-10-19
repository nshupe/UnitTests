import requests
import redis
import pygal
from flask import Flask
from datetime import datetime, timedelta
import userInput

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# api_symbol = userInput.get_stock_symbol()
# graph_type = userInput.get_chart_type()
# api_timeSeries = userInput.get_time_series()
# api_timeframe = "2009-01"
# api_start_date = userInput.get_start_date()
# api_end_date = userInput.get_end_date(api_start_date)

#this is for testing purposes
api_symbol = "IBM"
api_timeSeries = "INTRADAY"
api_timeframe = "2009-02"
graph_type = "Line"


beginning_date = "2009-01-01"
end_date = "2009-01-30"


# these arrays will be used to populate the y axis
open_array = []
high_array = []
low_array = []
close_array = []

# extract_x_axis will populate and convert to array once the loop for data runs
datetime_array = []

r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{api_timeSeries}&symbol={api_symbol}&outputsize=full&month={api_timeframe}&interval=5min&apikey=V33ZAOO7VB64CV9C')
all_data = r.json()

# switch statement since the json is diffrennt depending on time series
match api_timeSeries:
    case "DAILY":
        data = all_data["Time Series (Daily)"]
    case "INTRADAY":
        data = all_data["Time Series (5min)"]
    case "WEEKLY":
        data = all_data["Weekly Time Series"]
    case "MONTHLY":
        data = all_data["Monthly Time Series"]
    case _:
        print("we fked up")

def Graph():
    global datetime_array
    extract_x_axis()
    
    # magic god chatgpt taught me this
    datetime_array = sorted(list(set(datetime_array)))
    #make sure this runs after the lists are cleaned up
    extract_y_axis()

    # check which graph to use
    if graph_type == "Line":     
        chart = pygal.Line(x_label_rotation=20)
    elif graph_type == "Bar":
        chart = pygal.Bar(x_label_rotation=20)
    else:
         print("we fked up somewhere")

    #title
    chart.title = f'chart name' 
    
    # x axis
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'),datetime_array)
    
    #y axis
    chart.add('Open', open_array) # adds a line each data is a data point on graph
    chart.add('High',  high_array)
    chart.add('Low',   low_array)
    chart.add('Close', close_array)

    chart.render() # finalizes the graph 

    return chart.render_response() # prints to http://localhost:5000/


#this gets the datetime array which is the x axis in the graph
def extract_x_axis():
    global datetime_array  # Declare datetime_array as a global variable
    for key in data: 
        date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        year = date_object.year
        month = date_object.month
        day =  date_object.day
        datetime_array.append(datetime(year,month,day))  

def extract_y_axis():
    # loop over datetime array to get the keys in order for the data object
    for key in datetime_array:
        # Add 11 hours to the key
        date_object = key + timedelta(hours=11)
        # Convert the datetime object back to a string
        newKey = date_object.strftime("%Y-%m-%d %H:%M:%S")

        # adds all the data to the relevant places and turns it into float for the graph
        open_array.append(float(data[newKey]["1. open"]))
        high_array.append(float(data[newKey]["2. high"]))
        low_array.append(float(data[newKey]["3. low"]))
        close_array.append(float(data[newKey]["4. close"]))

@app.route('/')
def main():
       return Graph()
    
