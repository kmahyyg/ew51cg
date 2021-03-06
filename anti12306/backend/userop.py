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
# Filename: userop.py
#

from dbop import *
from uuid import uuid4 as uuidgen
from respmodel import *
from sqlalchemy.orm.exc import *
from sqlalchemy.exc import *
import flask
from hashlib import md5

TOKEN_EXPIRE_TIME = 86400
global db_session
db_session = create_db_conn()


def user_num2desc(status):
    if isinstance(status, int):
        if status == 0:
            return "normal user"
        elif status == 1:
            return "fraud user - banned"
        elif status == 8:
            return "vip user"
        elif status == 9:
            return "administrator"
        else:
            return "unknown"
    else:
        return None


def login_process(usrobj, login_password):
    if isinstance(usrobj, User):
        user_salt = usrobj.salt.encode()
        login_pwd = login_password.encode()
        server_logged_pwd = usrobj.password
        current_pwd = md5(login_pwd + user_salt).hexdigest()
        if current_pwd == server_logged_pwd:
            if usrobj.break_law == 0:
                return 0
            else:
                return -2
        else:
            return -1


def frontend_token_renew(usrobj):
    if isinstance(usrobj, User):
        usrnm = usrobj.username
        try:
            # get the current session token
            session_lst = db_session.query(Session).filter_by(username=usrnm).all()
            newtkn = str(uuidgen())
            if len(session_lst) > 1:
                for outdated in session_lst:
                    db_session.delete(outdated)
                    db_session.commit()
                cur_ses = Session(username=usrnm, usrtoken=newtkn)
                db_session.add(cur_ses)
                db_session.commit()
                return cur_ses.usrtoken
            elif len(session_lst) == 1:
                # validate if expired
                current_session = session_lst[0]
                if int(time()) - current_session.logged > TOKEN_EXPIRE_TIME:
                    db_session.delete(current_session)
                    db_session.commit()
                    # after invalidated, create
                    cur_ses = Session(username=usrnm, usrtoken=newtkn)
                    db_session.add(cur_ses)
                    db_session.commit()
                    return cur_ses.usrtoken
                else:
                    return current_session.usrtoken
            else:
                # session not exists, create a new one
                cur_ses = Session(username=usrnm, usrtoken=newtkn)
                db_session.add(cur_ses)
                db_session.commit()
                return cur_ses.usrtoken
        except:
            return "-5"


def check_batcredential(usrreq):
    try:
        usr_token = usrreq.headers['X-User-Token']
    except KeyError:
        usr_token = None
    try:
        usr_apikey = usrreq.headers['X-APIKEY']
    except KeyError:
        usr_apikey = None
        # Check existence
    if usr_apikey is None and usr_token is None:
        data = (None, -1)
        return data
    elif usr_apikey is None:
        # VALIDATE TOKEN, Token must be validated first.
        # If passed, return 1, else return -2.
        # If current_user is admin, return 9. If is_vip == True, return 8.
        # Return Format: Tuple (Username, ValidateStatus)
        try:
            current_sess = db_session.query(Session).filter_by(usrtoken=usr_token).one()
            if int(time()) - current_sess.logged > TOKEN_EXPIRE_TIME:
                # Token expired, please relogin.
                db_session.delete(current_sess)
                try:
                    db_session.commit()
                except InvalidRequestError as e:
                    print(e)
                    db_session.rollback()
                    db_session.commit()
                data = (None, -2)
                return data
            else:
                # Token validated, go on
                current_user = db_session.query(User).filter_by(username=current_sess.username).one()
                if current_user.break_law == 0:
                    if current_user.is_vip == 9:
                        data = (current_user.username, 9)
                        return data
                    elif current_user.is_vip == 8:
                        data = (current_user.username, 8)
                        return data
                    else:
                        data = (current_user.username, 0)
                        return data
                else:
                    raise NoResultFound
        except NoResultFound:
            data = (None, -2)
            return data
    else:
        # VALIDATE APIKEY
        # If passed, return 2, else return -2.
        # Return Format: Tuple (Username, validateStatus)
        try:
            current_user = db_session.query(User).filter(User.apikey == usr_apikey).one()
            data = (current_user.username, 2)
            return data
        except NoResultFound:
            data = (None, -2)
            return data


def get_userstats(authresp):
    if authresp[0] is not None:
        return db_session.query(User).filter_by(username=authresp[0]).one()
    else:
        raise LookupError("The user stats error occured: Internal Error!")
