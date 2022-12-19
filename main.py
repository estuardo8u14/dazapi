from flask import Flask, request
from flask_cors import CORS, cross_origin
#Import ccxt
#Para futuro si queremos que ejecute ordenes automatizadas por binance
""" PASSWORD = 'your_password'
API_KEY = 'your_api_key' 
API_SECRET = 'your_secret_key' """






app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

@app.route("/")
@cross_origin()
def root():
    return "OK"

@app.route("/alerta", methods=['POST'])
@cross_origin()
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


#https://dazapi.herokuapp.com/alerta

#mensaje de tradingview 
""" {
"time": {{time}},
"exchange":  {{exchange}},
"ticker": {{ticker}},
"texto": "Alert! Short-Venta"
} """