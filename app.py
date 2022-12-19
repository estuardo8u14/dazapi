from flask import Flask, request

app = Flask(__name__)

@app.route("/alerta", methods=['POST'])

def alerta():

    msg = request.json
    asset = msg['ticker']
    print(asset)

    return {
        'code': 'Success',
        'msg': msg
    }

