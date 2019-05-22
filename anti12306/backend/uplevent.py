#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

from uuid import uuid4 as uuidgen
from dbop import *
from sqlalchemy.exc import *

global db_session
db_session = create_db_conn()


def mark_as_waiting(eventid, username):
    try:
        suspecious_event = db_session.query(UploadEvent).filter_by(eventid=eventid).one()
        if suspecious_event.username == username:
            suspecious_event.status = 4
            try:
                db_session.commit()
            except InvalidRequestError as e:
                print(e)
                db_session.rollback()
                db_session.commit()
                return -1
            return 0
        else:
            return -2
    except:
        return -1
