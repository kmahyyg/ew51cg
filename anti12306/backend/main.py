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
from datetime import datetime
from bankcomm import *
from secrets import token_hex as saltgen
from secrets import token_urlsafe as pwdgen
from hashlib import md5

app = Flask(__name__)

global db_session
db_session = create_db_conn()


@app.route('/api/user/getHistory', methods=['GET'])
def get_recog_history():
    user_auth = check_batcredential(request)
    basic_result = {"username": user_auth[0], "uploadevents": []}
    if user_auth[1] >= 0:
        historylst = db_session.query(UploadEvent).filter_by(username=user_auth[0]).all()
        if len(historylst) > 0:
            for event in historylst:
                event_id = event.eventid
                ts = datetime.fromtimestamp(int(event.upltime)).strftime('%Y-%m-%d %H:%M:%S')
                if user_auth[1] == 8:
                    actual_cost = float(event.chnchars * 8.0 * 0.8)
                elif user_auth[1] == 9:
                    actual_cost = float(0.0)
                elif user_auth[1] == 2:
                    return make_response(jsonify(errResponse(-1, "This method is not allowed to be accessed in batch."))
                                         , 403)
                else:
                    actual_cost = float(event.chnchars * 8.0)
                basic_result["uploadevents"].append(
                    uploadEventResponse(
                        eventid=event_id, timestamp=ts, cost=actual_cost
                    )
                )
            return make_response(jsonify(basic_result), 200)
        else:
            return make_response(jsonify(basic_result), 200)
    else:
        return make_response(jsonify(errResponse(-1, "Invalid Credentials")), 403)


@app.route('/api/user/login', methods=['POST'])
def userlog():
    # extract user login form
    try:
        usercreds_nm = request.form['username']
        usercreds_pw = request.form['password']
        usercreds_time = request.form['_']
        if int(time()) - int(usercreds_time) > REPLAY_TIMEOUT:
            raise KeyError
    except KeyError:
        return make_response(jsonify(errResponse(-1, "Invalid request!")), 400)
    # check user's credentials
    try:
        current_user = db_session.query(User).filter_by(username=usercreds_nm).one()
        user_activated = login_process(current_user, usercreds_pw)
        if user_activated < 0:
            return make_response(jsonify(errResponse(user_activated, "Permission Denied.")), 403)
        else:
            # get existing session, if null, create
            # else, check if expired, revoke and regenerate
            new_token = frontend_token_renew(current_user)
            if new_token != "-5":
                return make_response(jsonify(authenticatedResponse(0, new_token)), 200)
            else:
                return make_response(jsonify(errResponse(-5, "Internal Error")), 500)
    except:
        return make_response(jsonify(errResponse(-1, "User credential is not correct!")), 403)


@app.route('/api/startOCR', methods=['POST'])
def batch_ocr2Text():
    # NOT DETECT REPLAY HERE: JUST LET USER PAY FOR WHAT THEY HAVE DONE!
    try:
        usr_photo = request.form['photo']  # Already encoded in base64.
        usr_photo = usr_photo[22:]  # remove the prefix of dataurl: "data:image/png;base64,"
    except KeyError:
        return make_response(jsonify(errResponse(-1, "Photo invalid.")), 400)
    user_auth = check_batcredential(request)
    if user_auth[1] >= 0:
        usrname = user_auth[0]
        cur_evntid = str(uuidgen())
        cur_usrobj = db_session.query(User).filter_by(username=usrname).one()
        if cur_usrobj.is_vip == 8 and cur_usrobj.balance > 150:
            result = comm_tensor(usr_photo)
            save_photo(usr_photo, cur_evntid)
            newEvent = UploadEvent()
            newEvent.username = usrname
            newEvent.eventid = cur_evntid
            newEvent.chnchars = result[1]
            newEvent.recoged = result[0]
            newEvent.upltime = int(time())
            db_session.add(newEvent)
            db_session.commit()
            if result[1] != 0:
                cur_usrobj.balance -= result[1] * 8 * 0.8
                db_session.commit()
                return make_response(jsonify(afterRecognitionResponse(
                    eventid=cur_evntid, retcode=0, retmsg=result[0], balance=cur_usrobj.balance
                )), 200)
            else:
                return make_response(jsonify(errResponse(-5, "Recognition failed.")), 500)
        elif cur_usrobj.is_vip == 0 and cur_usrobj.balance > 150:
            result = comm_tensor(usr_photo)
            save_photo(usr_photo, cur_evntid)
            newEvent = UploadEvent()
            newEvent.username = usrname
            newEvent.eventid = cur_evntid
            newEvent.chnchars = result[1]
            newEvent.recoged = result[0]
            newEvent.upltime = int(time())
            db_session.add(newEvent)
            db_session.commit()
            if result[1] != 0:
                cur_usrobj.balance -= result[1] * 8
                db_session.commit()
                return make_response(jsonify(afterRecognitionResponse(
                    eventid=cur_evntid, retcode=0, retmsg=result[0], balance=cur_usrobj.balance
                )), 200)
            else:
                return make_response(jsonify(errResponse(-5, "Recognition failed.")), 500)
        elif cur_usrobj.is_vip == 9:
            result = comm_tensor(usr_photo)
            save_photo(usr_photo, cur_evntid)
            newEvent = UploadEvent()
            newEvent.username = usrname
            newEvent.eventid = cur_evntid
            newEvent.chnchars = result[1]
            newEvent.recoged = result[0]
            newEvent.upltime = int(time())
            db_session.add(newEvent)
            db_session.commit()
            if result[1] != 0:
                return make_response(jsonify(afterRecognitionResponse(
                    eventid=cur_evntid, retcode=0, retmsg=result[0], balance=cur_usrobj.balance
                )), 200)
            else:
                return make_response(jsonify(errResponse(-5, "Recognition failed.")), 500)
        else:
            return make_response(jsonify(errResponse(-3, "Insufficient account balance.")), 400)
    else:
        return make_response(jsonify(errResponse(-1, "Permission Denied")), 403)


@app.route('/api/user/logout', methods=['GET'])
def logout():
    # verify the host, then directly remove session in db
    # will not do the user verification
    if request.host == 'anti12306.55lovecn.top':
        try:
            now_token = request.headers['X-User-Token']
            try:
                now_sess = db_session.query(Session).filter_by(usrtoken=now_token).one()
                db_session.delete(now_sess)
                db_session.commit()
                return make_response('', 200)
            except NoResultFound:
                pass
            except MultipleResultsFound:
                pass
            except InvalidRequestError:
                db_session.rollback()
                db_session.commit()
        except KeyError:
            return make_response('', 403)
    else:
        return make_response('', 400)


@app.route('/api/user/createOrder', methods=['POST'])
def createOrd():
    user_auth = check_batcredential(request)
    if user_auth[1] >= 0:
        orderData = request.json
        orderid = writeOrderData(orderData)
        if orderid != None:
            datadict = orderResponse(0, orderid)
            return make_response(jsonify(datadict), 200)
        else:
            return make_response(jsonify(errResponse(-5, "Server validate error, check your input.")), 500)
    else:
        return make_response(jsonify(errResponse(-1, "Invalid Credentials")), 403)


@app.route('/api/user/checkOrder', methods=['GET'])
def checkOrd():
    user_auth = check_batcredential(request)
    if user_auth[1] >= 0:
        try:
            orderID = request.form['orderID']
        except KeyError:
            return make_response(jsonify(errResponse(-1, "Invalid submit data")), 403)
        payment_status = check_payment(orderID)
        try:
            if payment_status["retcode"] != 0:
                return make_response(jsonify(errResponse(-5, "Server validate error, check your input.")), 500)
            else:
                return make_response(jsonify(payment_status), 403)
        except KeyError:
            return make_response(jsonify(payment_status), 200)
    else:
        return make_response(jsonify(errResponse(-1, "Invalid Credentials")), 403)


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
        if int(time()) - int(timestamp) > REPLAY_TIMEOUT:
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
    user_auth = check_batcredential(request)
    if user_auth[1] == 9:
        waiting_to_review = db_session.query(UploadEvent).filter_by(status=4).all()
        if len(waiting_to_review) > 0:
            resultdict = {
                "retcode": 0,
                "uploadevents": []
            }
            for events in waiting_to_review:
                eachEvent = reviewUpldEvent(events)
                resultdict["uploadevents"].append(eachEvent)
            return make_response(jsonify(resultdict), 200)
        else:
            return make_response('', 204)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/admin/review', methods=['POST'])
def admin_approve():
    user_auth = check_batcredential(request)
    if user_auth[1] == 9:
        eventid = request.form['eventid']
        event_proc = request.form['op']
        modified = db_session.query(UploadEvent).filter_by(eventid=eventid).one()
        modified.status = int(event_proc)
        db_session.commit()
        return make_response(jsonify(errResponse(0, "Proceeded.")), 200)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/admin/reset', methods=['POST'])
def admin_resetuser():
    user_auth = check_batcredential(request)
    if user_auth[1] == 9:
        req_username = request.form['username']
        n_pwd = pwdgen(8)
        n_salt = saltgen(8)
        n_apikey = str(uuidgen())
        n_hashpwd = md5(n_pwd.encode() + n_salt.encode()).hexdigest()
        # check if user exists
        try:
            # refresh the password
            # if exists, update
            # if not exists, error
            corr_user = db_session.query(User).filter_by(username=req_username).one()
            corr_user.password = n_hashpwd
            corr_user.salt = n_salt
            corr_user.apikey = n_apikey
            corr_user.break_law = 0
            db_session.commit()
            # delete online sessions
            all_cur_user_sessions = db_session.query(Session).filter_by(username=req_username).all()
            if len(all_cur_user_sessions) > 0:
                for online in all_cur_user_sessions:
                    db_session.delete(online)
                    db_session.commit()
            return make_response(jsonify(
                {
                    "retcode": 0,
                    "username": req_username,
                    "password": n_pwd,
                    "apikey": corr_user.apikey
                }
            ), 200)
        except:
            return make_response(jsonify(errResponse(-2, "Your username is invalid.")), 400)
    else:
        return make_response(jsonify(errResponse(-1, "No valid credential")), 403)


@app.route('/api/cron', methods=['OPTIONS'])
def cronjob():
    # This is used for daily job, cleanup user session and refund
    authed_site = request.headers["Origin"]
    if authed_site == "127.0.0.1" and request.headers['User-Agent'][:6] == "curl/7":
        try:
            # Clean expired user session on the frontend
            all_sessions = db_session.query(Session).all()
            if len(all_sessions) > 0:
                toexpire = []
                for sess in all_sessions:
                    if int(time()) - sess.logged > TOKEN_EXPIRE_TIME:
                        toexpire.append(sess)
                for expired in toexpire:
                    db_session.delete(expired)
                db_session.commit()
            else:
                pass
            # Refund will be done in each day 24:00
            all_failed_recognition = db_session.query(UploadEvent).filter_by(status=2).all()
            if len(all_failed_recognition) > 0:
                # get user id
                for event in all_failed_recognition:
                    corresponding_user = db_session.query(User).filter_by(username=event.username).one()
                    VIP_identify = corresponding_user.is_vip
                    refund_cost = 0.0
                    if VIP_identify > 0:
                        refund_cost = event.chnchars * 0.8 * 8
                    else:
                        refund_cost = event.chnchars * 1.0 * 8
                    corresponding_user.balance += refund_cost
                    db_session.delete(event)
                    db_session.commit()
            else:
                pass
            # cleanup unpaid orders after 24h
            all_expired_orders = db_session.query(Order).filter_by(status=1).all()
            if len(all_expired_orders) > 0:
                for order in all_expired_orders:
                    if int(time()) - order.submitat > TOKEN_EXPIRE_TIME:
                        db_session.delete(order)
                        db_session.commit()
                    else:
                        pass
            else:
                pass
            # set fraud user to illegal
            all_fraud_events = db_session.query(UploadEvent).filter_by(status=3).all()
            if len(all_fraud_events) > 0:
                for event in all_fraud_events:
                    corresponding_user = db_session.query(User).filter_by(username=event.username).one()
                    corresponding_user.break_law = 1
                    db_session.commit()
            else:
                pass
            return make_response('', 204)
        except:
            return make_response(jsonify(errResponse(-5, "Internal Error")), 500)
    else:
        abort(403)


@app.route('/api/payment/callback', methods=['POST'])
def recv_payment_callback():
    # TODO: reserved for process payment gateway response
    process_gateway(request)
    return make_response(jsonify(errResponse(-1, "Under Construction")), 200)


@app.teardown_appcontext
def shutdown_dbpool(exception=None):
    db_exit(db_session)


app.run(host='0.0.0.0', port=8080, debug=False)
