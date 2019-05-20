#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
# anti12306-web-backend
# Copyright (C) 2019  kmahyyg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Filename: main.py
#

REPLAY_TIMEOUT = 15

from flask import Flask, jsonify, request, make_response
from dbop import *
from respmodel import *
from userop import *
from uplevent import *
from payment import *

app = Flask(__name__)

db_session = create_db_conn()


@app.route('/api/user/login', methods=['POST'])
def userlog():
    # extract user login form
    usercreds_nm = request.form['username']
    usercreds_pw = request.form['password']
    usercreds_time = request.form['_']
    # get existing session, if null, create
    # else, check if expired, revoke and regenerate


@app.route('/api/startOCR', methods=['POST'])
def batch_ocr2Text():
    # Get OCR result of uploaded photo
    # photo is a base64 encoded string
    photo_b64 = request.form['photo']
    photo_time = request.form['timestamp']
    # Credential check
    try:
        usr_token = request.headers['X-User-Token']
    except KeyError:
        usr_token = None
    try:
        usr_apikey = request.headers['X-APIKEY']
    except KeyError:
        usr_apikey = None
    if usr_apikey is None:
        usr_secret = usr_token
    else:
        usr_secret = usr_apikey


@app.route('/api/user/logout', methods=['GET'])
def logout():
    revoked_token = request.headers['X-User-Token']


@app.route('/api/user/createOrder', methods=['POST'])
def createOrd():
    orderData = request.json
    order_usr = orderData['username']
    order_amount = float(orderData['amount'])
    order_paygate = orderData['payment']


@app.route('/api/user/checkOrder', methods=['GET'])
def checkOrd():
    orderID = request.form['orderID']


@app.route('/api/user/checkBalance', methods=['GET'])
def batch_balance():
    try:
        usr_token = request.headers['X-User-Token']
    except KeyError:
        usr_token = None
    try:
        usr_apikey = request.headers['X-APIKEY']
    except KeyError:
        usr_apikey = None
    if usr_apikey is None:
        usr_secret = usr_token
    else:
        usr_secret = usr_apikey


@app.route('/api/user/getUser', methods=['GET'])
def dashboard_usr():
    usr_token = request.headers['X-User-Token']


@app.route('/api/report/error', methods=['POST'])
def incorrect_recg():
    # incorrect recognition, call maintainers and go to check
    try:
        eventid = request.form['eventid']
        timestamp = request.form['timestamp']
        if int(time()) - timestamp > REPLAY_TIMEOUT:
            raise KeyError
    except KeyError:
        return make_response(jsonify(errResponse(-1, "Invalid Data!")), 400)
    try:
        usr_token = request.headers['X-User-Token']
    except KeyError:
        usr_token = None
    try:
        usr_apikey = request.headers['X-APIKEY']
    except KeyError:
        usr_apikey = None

    if usr_apikey is None and usr_token is None:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)
    elif usr_apikey is None:
        usr_secret = usr_token
    else:
        usr_secret = usr_apikey
    if check_credential(usr_secret):
        try:
            mark_as_waiting(eventid)
            return make_response(jsonify(errResponse(0, "Received, waiting for manual review.")), 200)
        except IndexError:
            return make_response(jsonify(errResponse(-2, "Your eventid is invalid")), 400)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/admin/review', methods=['GET'])
def review_report():
    pass


@app.route('/api/payment/callback', methods=['POST'])
def recv_payment_callback():
    # This route is preserved for webhook to receive the response of
    # the callback after payment successfully finished.
    #
    # Always successful for test.
    return make_response(jsonify(errResponse(-1, "Under Construction")), 200)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_exit(db_session)


app.run(host='0.0.0.0', port=8080, debug=True)
