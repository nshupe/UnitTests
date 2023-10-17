import requests
import redis
import pygal
from flask import Flask
from datetime import datetime, timedelta
import userInput

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

api_symbol = userInput.get_stock_symbol()
graph_type = userInput.get_chart_type()
api_timeSeries = userInput.get_time_series()
api_timeframe = "2009-01"
api_start_date = userInput.get_start_date()
api_end_date = userInput.get_end_date(api_start_date)


beginning_date = "2009-01-01"
end_date = "2009-01-30"

# example will populate the actualy array once the loop for data runs
datetime_array = []

r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{api_timeSeries}&symbol={api_symbol}&outputsize=full&month={api_timeframe}&interval=5min&apikey=V33ZAOO7VB64CV9C')
all_data = r.json()
data = all_data["Time Series (5min)"]

#this gets the datetime array which is the x axis in the graph
def extract_x_axis():
    for key in data: 
        date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        year = date_object.year
        month = date_object.month
        day =  date_object.day
        print (datetime(year,month,day))
        datetime_array.append(datetime(year,month,day))  

@app.route('/')
def Line_graph():
    extract_x_axis()
    unique_list = list(set(datetime_array))
    chart = pygal.Line()
    chart.title = 'chart name' # title
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'),unique_list)
    
    chart.add('Open', [1,2,3,4,5]) # adds a line each data is a data point on graph
    chart.add('High',  [])
    chart.add('Low',   [])
    chart.add('Close', [])

    chart.render() # finalizes the graph 

    return chart.render_response() # prints to screen


