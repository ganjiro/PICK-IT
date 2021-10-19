import ast
import time
from flask import Flask, render_template, request
import json
from redis_connector import Connection

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    url = "redis://:p975d2dba3a5c75f5d5fc51a412f07722e4be526860ae94609067b37cd08adb7d@ec2-54-156-199-127.compute-1.amazonaws.com:17169"
    Connection.instance().set_url(url)
    return render_template('index.html')


@app.route('/code', methods=["POST"])
def checkcode():
    ret_value = False
    value = request.form.get("id")
    conn = Connection.instance()

    conn.set_code(value)
    conn.set("ACK")
    time.sleep(1)
    resp = conn.get()

    if resp and resp == "RACK":
        ret_value = True
    else:
        conn.reset_code()

    return json.dumps({'success': ret_value}), 200, {'ContentType': 'application/json'}

@app.route('/lock', methods=["POST"])
def lockchamp():
    conn = Connection.instance()

    value = request.form.get("id")
    try:
        int(value)
    except:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

    conn.set(value,'_champ')

    a = conn.get('_champ')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/check_gamestart', methods=["POST"])
def check_gamestart():
    ret_value = False
    conn = Connection.instance()

    resp = conn.get("_gamephase")

    if resp and resp != "Matchmaking":
        ret_value = True

    return json.dumps({'success': ret_value}), 200, {'ContentType': 'application/json'}


@app.route('/waiting', methods=["GET"])
def next_code():
    return render_template('waiting.html')

@app.route('/champselection', methods=["GET"])
def champselection():
    return render_template('champselection.html')

@app.route('/check_gamestatus', methods=["POST"])
def check_gamestatus():

    conn = Connection.instance()
    #conn.set_code("F")  # todo remove
    phase = conn.get("_gamephase")

    if phase and phase == "Matchmaking":
        return render_template('waiting.html')

    resp = conn.get("_gamestatus")

    try:
        resp = ast.literal_eval(resp)
    except:
        return {}, 400, {'ContentType': 'application/json'}
    resp['gamephase'] = phase

    return json.dumps(resp), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
