from flask import Flask, request
from flask_cors import cross_origin, CORS
import mysql.connector
from pydantic import BaseModel
from twilio.rest import Client 
 


#Import ccxt
#Para futuro si queremos que ejecute ordenes automatizadas por binance
""" PASSWORD = 'your_password'
API_KEY = 'your_api_key' 
API_SECRET = 'your_secret_key' """

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def root():
    return {
        'Code': 'Conectado'
    }

@app.route("/alerta", methods=['POST', 'GET'])
@cross_origin()
def alerta():

    
    msg = request.json
    time = msg['time']
    exchange = msg['exchange']
    ticker = msg['ticker']
    texto = msg['texto']
    precio = msg['precio']



    return {
        'Code1': 'Exitosa',
        'Tiempo1': time,
        'Exchange1': exchange,
        'Ticker1': ticker,
        'Texto1': texto,
        'Precio1': precio
    }

@app.route("/post_alerta", methods=['POST'])
@cross_origin()
def post_alerta():
    data = request.get_json()
    time = data['time']
    exchange = data['exchange']
    ticker = data['ticker']
    precio = data['precio']
    indicadores = data['indicadores']
    texto = data['texto']

    
    
    #whatsapp
    account_sid = 'AC6e062b7d696ef5104f95ecebb202aae6' 
    auth_token = 'b1ebc41cf5eb9c956bf9f9f3ac526ee0' 
    client = Client(account_sid, auth_token) 
 
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body= data['texto'],      
                              to='whatsapp:+50241067266' 
                          ) 
 
    print(message.sid)

    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5585708",
        password="dslZ3LQlhu",
        database="sql5585708"
    )
    print(type(data))

    mycursor = mydb.cursor()

    sql = "INSERT INTO notifs" + " (time, exchange, ticker, precio, indicadores, texto) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (
        data['time'],
        data['exchange'],
        data['ticker'],
        data['precio'],
        data['indicadores'],
        data['texto']
    )
    mycursor.execute(sql, (val))

    mydb.commit()

    if(int(mycursor.rowcount) > 0):
        return data
    
    else:
        return False

@app.route("/get_alerta", methods=["GET"])
@cross_origin()
def get_alerta():
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5585708",
        password="dslZ3LQlhu",
        database="sql5585708"
    )
    mycursor = mydb.cursor()

    sql = "SELECT id, time, exchange, ticker, precio, indicadores, texto FROM notifs WHERE id= (SELECT MAX(id) FROM notifs)"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    
    data = []

    for result in results:
        dict = {}
        dict["id"] = result[0]
        dict["time"] = result[1]
       
        dict["exchange"] = result[2]
        dict["ticker"] = result[3]
        dict["precio"] = result[4]

        dict["indicadores"] = result[5]
        dict["texto"] = result[6]

        data.append(dict)

    print(data)
    return dict

#get mensaje en forma correcta para whatsappAPI


#send de mensaje ppor whatsapp




#https://dazapi.herokuapp.com/alerta

#mensaje de tradingview 
""" {
"time": {{time}},
"exchange":  {{exchange}},
"ticker": {{ticker}},
"texto": "Alert! Short-Venta"
} """





""" # initialize our Flask application
from logging import getLogger, DEBUG

from flask import Flask, request, jsonify, render_template, Response

from commons import VERSION_NUMBER, LOG_LOCATION
from components.actions.base.action import am
from components.events.base.event import em
from components.logs.log_event import LogEvent
from components.schemas.trading import Order, Position
from utils.log import get_logger
from utils.register import register_action, register_event, register_link

# register actions, events, links
from settings import REGISTERED_ACTIONS, REGISTERED_EVENTS, REGISTERED_LINKS

registered_actions = [register_action(action) for action in REGISTERED_ACTIONS]
registered_events = [register_event(event) for event in REGISTERED_EVENTS]
registered_links = [register_link(link, em, am) for link in REGISTERED_LINKS]

app = Flask(__name__)

# configure logging
logger = get_logger(__name__)

schema_list = {
    'order': Order().as_json(),
    'position': Position().as_json()
}


@app.route("/", methods=["GET"])
def dashboard():
    if request.method == 'GET':

        # check if gui key file exists
        try:
            with open('.gui_key', 'r') as key_file:
                gui_key = key_file.read().strip()
                # check that the gui key from file matches the gui key from request
                if gui_key == request.args.get('guiKey', None):
                    pass
                else:
                    return 'Access Denied', 401

        # if gui key file does not exist, the tvwb.py did not start gui in closed mode
        except FileNotFoundError:
            logger.warning('GUI key file not found. Open GUI mode detected.')

        # serve the dashboard
        action_list = am.get_all()
        return render_template(
            template_name_or_list='dashboard.html',
            schema_list=schema_list,
            action_list=action_list,
            event_list=registered_events,
            version=VERSION_NUMBER
        )


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            logger.error(f'Error getting JSON data from request...')
            logger.error(f'Request data: {request.data}')
            logger.error(f'Request headers: {request.headers}')
            return 'Error getting JSON data from request', 400

        logger.info(f'Request Data: {data}')
        triggered_events = []
        for event in em.get_all():
            if event.webhook:
                if event.key == data['key']:
                    event.trigger(data=data)
                    triggered_events.append(event.name)

        if not triggered_events:
            logger.warning(f'No events triggered for webhook request {request.get_json()}')
        else:
            logger.info(f'Triggered events: {triggered_events}')

    return Response(status=200)


@app.route("/logs", methods=["GET"])
def get_logs():
    if request.method == 'GET':
        log_file = open(LOG_LOCATION, 'r')
        logs = [LogEvent().from_line(log) for log in log_file.readlines()]
        return jsonify([log.as_json() for log in logs])


@app.route("/event/active", methods=["POST"])
def activate_event():
    if request.method == 'POST':
        # get query parameters
        event_name = request.args.get('event', None)

        # if event name is not provided, or cannot be found, 404
        if event_name is None:
            return Response(f'Event name cannot be empty ({event_name})', status=404)
        try:
            event = em.get(event_name)
        except ValueError:
            return Response(f'Cannot find event with name: {event_name}', status=404)

        # set event to active or inactive, depending on current state
        event.active = request.args.get('active', True) == 'true'
        logger.info(f'Event {event.name} active set to: {event.active}, via POST request')
        return {'active': event.active}


if __name__ == '__main__':
    app.run(debug=True) """