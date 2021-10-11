import threading
import time
from flask import Flask, render_template, request
import redis
import json

app = Flask(__name__)

url = "redis://:p975d2dba3a5c75f5d5fc51a412f07722e4be526860ae94609067b37cd08adb7d@ec2-54-156-199-127.compute-1.amazonaws.com:17169"
r = redis.from_url(url)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/code', methods=["POST", "GET"])
def index_():
    ret_value = False
    value = request.form.get("id")

    r.set(value, "ACK")
    time.sleep(1)
    resp = r.get(value)

    if resp and str(resp.decode("UTF-8"))=="RACK":
        ret_value = True

    return json.dumps({'success': ret_value}), 200, {'ContentType': 'application/json'}


@app.route('/next_code', methods=["GET"])
def sus():
    code = request.args.get('code', default=1, type=str)
    return str(code)


if __name__ == '__main__':
    app.run(debug=True)
