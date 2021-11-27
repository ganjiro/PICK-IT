import ast
import datetime
import json
import os
import time
from urllib.parse import urlparse

from flask import Flask, render_template, request, make_response

from redis_connector import Connection

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    url = urlparse(os.environ.get("REDIS_URL"))
    Connection.instance().set_url(url)
    if url != '':
        return render_template('index.html')
    else:
       return render_template('champselection.html')


@app.route('/code', methods=["POST"])
def checkcode():
    ret_value = False

    code = request.form.get("id").upper()
    conn = Connection.instance()

    conn.set(code, "ACK")
    time.sleep(1)
    resp = conn.get(code)

    if resp and resp == "RACK":
        ret_value = True

    return json.dumps({'success': ret_value}), 200, {'ContentType': 'application/json'}


@app.route('/setcookie', methods=["POST"])
def set_cookie():
    value = request.form.get("code").upper()

    res = make_response("<h1>cookie is set</h1>")
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=90)
    res.set_cookie("code", value, expires=expire_date)
    return res


@app.route('/lock', methods=["POST"])
def lockchamp():
    conn = Connection.instance()

    value = request.form.get("id")
    try:
        int(value)
    except:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    code = request.cookies.get('code')
    conn.set(str(code) + '_champ', value)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/set_pickable', methods=["POST"])
def check_pickable():
    conn = Connection.instance()

    code = request.cookies.get('code').upper()

    resp = conn.get(str(code) + "_pickable")

    try:
        resp = ast.literal_eval(resp)
    except:
        return {}, 400, {'ContentType': 'application/json'}

    return json.dumps(resp), 200, {'ContentType': 'application/json'}


@app.route('/check_gamestart', methods=["POST"])
def check_gamestart():
    ret_value = False
    closed = False
    conn = Connection.instance()

    code = request.cookies.get('code').upper()
    resp = conn.get(str(code) + "_gamephase")

    if resp and resp != "Matchmaking":
        ret_value = True

    if resp == 'Closed':
        closed = True

    return json.dumps({'success': ret_value, 'closed': closed}), 200, {'ContentType': 'application/json'}


@app.route('/waiting', methods=["GET"])
def next_code():
    return render_template('waiting.html')


@app.route('/champselection', methods=["GET"])
def champselection():
    return render_template('champselection.html')


@app.route('/getcookie', methods=["POST"])
def getcookie():
    code = request.cookies.get('code').upper()

    if not code:
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': True, 'code': code}), 200, {'ContentType': 'application/json'}


@app.route('/check_gamestatus', methods=["POST"])
def check_gamestatus():
    conn = Connection.instance()

    code = request.cookies.get('code').upper()
    phase = conn.get(str(code) + "_gamephase")

    resp = conn.get(str(code) + "_gamestatus")

    try:
        resp = ast.literal_eval(resp)
    except:
        return {"gamephase": phase}, 200, {'ContentType': 'application/json'}

    resp['gamephase'] = phase

    return json.dumps(resp), 200, {'ContentType': 'application/json'}


@app.route('/get_redis_connection', methods=["GET"])
def get_redis_connection():
    url = urlparse(os.environ.get("REDIS_URL"))
    return {"URL": url}, 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
