from flask import Flask, request
#Import ccxt
#Para futuro si queremos que ejecute ordenes automatizadas por binance
""" PASSWORD = 'your_password'
API_KEY = 'your_api_key' 
API_SECRET = 'your_secret_key' """




app = Flask(__name__)



@app.route("/alerta", methods=['POST'])

def alerta():

    msg = request.json
    tiempo = msg['time']
    exchange = msg['exchange']
    ticker = msg['ticker']
    texto = msg['texto']
    print(tiempo)
    print(exchange)
    print(ticker)
    print(texto)



    return {
        'code': 'Exitosa',
        'msg': msg
    }

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

    
#mensaje de tradingview
""" {
"time": {{time}},
"exchange":  {{exchange}},
"ticker": {{ticker}},
"texto": "Alert! Short-Venta"
} """