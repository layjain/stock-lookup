from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def stock_lookup():
    if request.method == 'POST':
        symbol = request.form['symbol']
        stock_data = yf.Ticker(symbol)
        history = stock_data.history(period='1y')

        fig = go.Figure(data=go.Candlestick(
            x=history.index,
            open=history['Open'],
            high=history['High'],
            low=history['Low'],
            close=history['Close']
        ))

        fig.update_layout(title=f'{symbol} - 52 Week Chart', xaxis_rangeslider_visible=False)
        chart_div = fig.to_html(full_html=False)
        high = max(history['High'])
        low = max(history['Low'])
        return render_template('result.html', chart_div=chart_div, high=high, low=low)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

