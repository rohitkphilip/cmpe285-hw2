import datetime
from pytz import timezone
from flask import Flask
from flask import render_template 
from flask import request
import requests
from alpha_vantage.timeseries import TimeSeries

# API KEY : M5HGCFRXZKVQZB7W
# #replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
# r = requests.get(url)
# data = r.json()

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def home():
    if request.method == 'POST':

        stock_symbol = request.form.get('symbol');
        try :

            result = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+stock_symbol+'&apikey=M5HGCFRXZKVQZB7W')
            data = result.json();
            company_name = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+stock_symbol+'&apikey=M5HGCFRXZKVQZB7W')
            full_name = company_name.json()['bestMatches'][0]['2. name']
            symbol = data['Global Quote']['01. symbol'];
            stock_price = data['Global Quote']['05. price'];
            value_change = data['Global Quote']['09. change'];
            percentage_change = data['Global Quote']['10. change percent'];

            
            now_utc = datetime.datetime.now(timezone('US/Pacific'))
            print('\nOutput : \n')

            fmt = "%a %b %d %H:%M:%S %Z %Y"  
            time = now_utc.strftime(fmt);


            stock_data = {
            'time' : time,
            'full_name' : full_name,
            'stock_price' : stock_price,
            'value_change' : float(value_change),
            'percentage_change' : percentage_change,
            }
            print(stock_data)
            return render_template('index.html', data = stock_data);
        except :
            return render_template('index.html', error = {'error' : 'API limit exceeded or Invalid Symbol.'});


    return render_template('index.html');


if __name__ == '__main__':
    app.run(debug = True)
