#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

from dbop import *
from uuid import uuid4 as uuidgen
from respmodel import *
from sqlalchemy.orm.exc import *
from sqlalchemy.exc import *
import flask

TOKEN_EXPIRE_TIME = 86400
global db_session


def check_batcredential(usrreq):
    if isinstance(usrreq, flask.request):
        # Check Type
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
            current_user = db_session.query(Session).filter(Session.usrtoken == usr_token).one()
            if current_user.logged - int(time()) > TOKEN_EXPIRE_TIME:
                # Token expired, please relogin.
                db_session.delete(current_user)
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
                if current_user.is_vip == 9:
                    data = (current_user.username, 9)
                    return data
                elif current_user.is_vip == 8:
                    data = (current_user.username, 8)
                    return data
                else:
                    data = (current_user.username, 0)
                    return data
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
