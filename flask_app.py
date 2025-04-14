from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import pandas as pd 

app = Flask(__name__)

def get_stock_data(symbol):
    api_key = 'HF09Q56KFM690UMA'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['Time Series (Daily)']

def plot_stock_data(data, chart_type, start_date, end_date):
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index() 
    
    df = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]
    
    dates = df.index
    prices = df['4. close'].astype(float)

    plt.figure(figsize=(10, 5))
    
    if chart_type == 'line':
        plt.plot(dates, prices, label='Closing Price')
    elif chart_type == 'bar':
        plt.bar(dates, prices, label='Closing Price')
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Over Time')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/stock_chart.png')
    plt.close()  

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        stock_symbol = request.form['symbol']
        chart_type = request.form['chart_type']  
        start_date = request.form['start_date']  
        end_date = request.form['end_date']     

        data = get_stock_data(stock_symbol)
        plot_stock_data(data, chart_type, start_date, end_date)

        return render_template(
            'index.html',
            symbols=['AAPL', 'GOOG', 'TSLA'],
            chart='static/stock_chart.png'
        )
    return render_template('index.html', symbols=['AAPL', 'GOOG', 'TSLA'])

if __name__ == '__main__':
    app.run(debug=True)

