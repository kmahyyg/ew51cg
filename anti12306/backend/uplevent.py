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
# Filename: uplevent.py
#

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
