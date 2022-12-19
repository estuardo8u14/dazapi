from flask import Flask, request
import ccxt
import config

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

#mensaje de tradingview
""" {
"time": {{time}},
"exchange":  {{exchange}},
"ticker": {{ticker}}",
"texto": "Alert! Short-Venta"
} """