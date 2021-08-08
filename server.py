#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import json
from flask import Flask, jsonify, request
from flask import render_template
from config import getServer
from sqlite import Executor
from logger import logger


app = Flask(__name__)
exector = Executor()

@app.route('/')
@app.route('/home')
def home():
    # return json.dumps(json.load(open('config.json', 'r', encoding='utf-8')), ensure_ascii=False, indent=1)
    return render_template('home.html')


@app.route('/save', methods=["POST"])
def save():
    try:
        data = is_json(request.json)
        logger.info(data)
        exector.save(data)
        return json.dumps({'code': 1, 'msg': 'successful', 'data': None})
    except Exception as err:
        return json.dumps({'code': 0, 'msg': err, 'data': None})


def is_json(data):
    try:
        for k, v in data.items():
            if k == 'name': continue
            data[k] = json.dumps(json.loads(v), ensure_ascii=False)
    except Exception as err:
        raise err
    return data



if __name__ == '__main__':
    app.run(host = getServer('IP'), port = int(getServer('port')))
