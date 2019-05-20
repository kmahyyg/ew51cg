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

from flask import Flask, jsonify, request, make_response, abort
from dbop import *
from respmodel import *
from userop import *
from uplevent import *
from payment import *

app = Flask(__name__)

global db_session
db_session = create_db_conn()


@app.route('/api/user/getHistory', methods=['GET'])
def get_recog_history():
    pass


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
    #TODO: Get user balance, must > 150 coins
    # Get OCR result of uploaded photo
    # photo is a base64 encoded string
    photo_b64 = request.form['photo']
    photo_time = request.form['timestamp']
    # Credential check


@app.route('/api/user/logout', methods=['GET'])
def logout():
    pass


@app.route('/api/user/createOrder', methods=['POST'])
def createOrd():
    orderData = request.json
    order_usr = orderData['username']
    order_amount = float(orderData['amount'])
    order_paygate = orderData['payment']


@app.route('/api/user/checkOrder', methods=['GET'])
def checkOrd():
    orderID = request.form['orderID']
    # TODO TO-BE-FINISHED


@app.route('/api/user/getUser', methods=['GET'])
def dashboard_usr():
    user_auth = check_batcredential(request)
    if user_auth[1] >= 0:
        current_user = get_userstats(user_auth)
        return make_response(jsonify(
            userStats(current_user.username, current_user.is_vip,
                      current_user.apikey, current_user.balance,
                      current_user.break_law)
        ), 200)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/report/error', methods=['POST'])
def incorrect_recg():
    # incorrect recognition, call maintainers and go to check
    try:
        eventid = request.form['eventid']
        timestamp = request.form['timestamp']
        if int(time()) - timestamp > REPLAY_TIMEOUT:
            raise KeyError
    except:
        return make_response(jsonify(errResponse(-1, "Invalid Data!")), 400)
    user_auth = check_batcredential(request)
    if user_auth[1] == -1:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)
    elif user_auth[1] == -2:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)
    elif user_auth[1] >= 0:
        # Authenticate passed
        event = mark_as_waiting(eventid, user_auth[0])
        if event == 0:
            return make_response(jsonify(errResponse(0, "Received, waiting for manual review.")), 200)
        else:
            return make_response(jsonify(errResponse(-2, "Your eventid is invalid or Server Error.")), 400)


@app.route('/api/admin/review', methods=['GET'])
def review_report():
    from base64 import b64encode
    user_auth = check_batcredential(request)
    if user_auth[1] == 9:
        waiting_to_review = db_session.query(UploadEvent).filter_by(UploadEvent.status == 4).all()
        if len(waiting_to_review) > 0:
            resultdict = {
                "retcode": 0,
                "uploadevents": []
            }
            for events in waiting_to_review:
                photo_data = "data:image/png;base64," + b64encode(open("userimgs/" + events.eventid + ".png", "rb").read()).decode()
                eachEvent = {"eventid": events.eventid, "photo": photo_data}
                resultdict["uploadevents"].append(eachEvent)
            return make_response(jsonify(resultdict), 200)
        else:
            return make_response(jsonify(errResponse(0, "No events waiting to be reviewed.")), 200)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/admin/review', methods=['POST'])
def admin_approve():
    user_auth = check_batcredential(request)
    if user_auth[1] == 9:
        eventid = request.form['eventid']
        modified = db_session.query(UploadEvent).filter_by(UploadEvent.eventid == eventid).one()
        modified.status = 2
        db_session.commit()
        return make_response(jsonify(errResponse(0, "Proceeded.")), 200)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/cron', methods=['POST'])
def cronjob():
    # This is used for daily job, cleanup user session and refund
    authed_site = request.headers["Origin"]
    if authed_site == "127.0.0.1" and request.user_agent[:6] == "curl/7":
        # Clean expired user session on the frontend
        all_sessions = db_session.query(Session).all()
        if len(all_sessions) > 0:
            toexpire = []
            for sess in all_sessions:
                if sess.timestamp - int(time()) > TOKEN_EXPIRE_TIME:
                    toexpire.append(sess)
            for expired in toexpire:
                db_session.delete(expired)
            db_session.commit()
        else:
            pass
        # Refund will be done in each day 24:00
        all_failed_recognition = db_session.query(UploadEvent).filter_by(UploadEvent.status == 2).all()
        if len(all_failed_recognition) > 0:
            # get user id
            for event in all_failed_recognition:
                corresponding_user = db_session.query(User).filter_by(User.username == event.username).one()
                VIP_identify = corresponding_user.is_vip
                refund_cost = 0.0
                if VIP_identify > 0:
                    refund_cost = event.chnchars * 0.7 * 15
                else:
                    refund_cost = event.chnchars * 1.0 * 15
                corresponding_user.balance += refund_cost
                db_session.commit()
        else:
            pass
    else:
        abort(403)


@app.route('/api/payment/callback', methods=['POST'])
def recv_payment_callback():
    return make_response(jsonify(errResponse(-1, "Under Construction")), 200)


@app.teardown_appcontext
def shutdown_dbpool(exception=None):
    db_exit(db_session)


app.run(host='0.0.0.0', port=8080, debug=True)
