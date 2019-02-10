import flask
from .db import MongoDB
import json


app = flask.Flask(__name__)
@app.route('/getFastestProxy')
def get_fastest():

    return MongoDB().get_fastest_proxy()\

@app.route('/getRandomProxy')
def get_random():

    return MongoDB().get_random_proxy()

@app.route('/getProxies')
def get_proxies():
    args = dict(flask.request.args)
    proxies = json.dumps(MongoDB().get(int(args['count'][0])))
    return proxies\


@app.route('/delete')
def delete():
    args = dict(flask.request.args)
    try:
        MongoDB().delete({'proxy':args['proxy'][0]})
        return '删除成功'
    except Exception:
        return '删除失败'


def api():
    app.run(port='12321')