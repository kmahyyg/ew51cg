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
# Filename: respmodel.py
#
# This file is response models according to swagger document.
# Working as a constructor-like object in Java.

from dbop import *
from userop import *


def errResponse(retcode, retmsg):
    if isinstance(retcode, int) and isinstance(retmsg, str):
        datadict = {"retcode": retcode, "retmsg": retmsg}
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def authenticatedResponse(retcode, token):
    if isinstance(retcode, int) and isinstance(token, str):
        datadict = {"retcode": retcode, "token": token}
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def uploadEventResponse(eventid, timestamp, cost):
    if isinstance(timestamp, int) and isinstance(cost, float):
        datadict = {"eventid": eventid, "timestamp": timestamp, "cost": cost}
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def userStats(username, is_vip, apikey, balance, illegal):
    if isinstance(is_vip, int) and isinstance(illegal, int) and isinstance(balance, float):
        datadict = {
            "username": username,
            "is_vip": user_num2desc(is_vip),
            "apikey": apikey,
            "balance": balance,
            "break_law": illegal
        }
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def orderResponse(retcode, orderid):
    if isinstance(retcode, int):
        datadict = {"retcode": retcode, "orderid": orderid}
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def afterPayResponse(orderid, timestamp, amount, resp):
    if isinstance(amount, float):
        datadict = {
            "orderid": orderid,
            "timestamp": timestamp,
            "amount": amount,
            "resp": resp
        }
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def afterRecognitionResponse(eventid, retcode, retmsg, balance):
    if isinstance(retcode, int) and isinstance(balance, float):
        datadict = {
            "eventid": eventid,
            "retcode": retcode,
            "retmsg": retmsg,
            "balance": balance
        }
        return datadict
    else:
        raise AssertionError("Illegal data input!")


def reviewUpldEvent(events):
    if events is not None and isinstance(events, UploadEvent):
        from base64 import b64encode
        photo_data = "data:image/png;base64," + b64encode(
            open("userimgs/" + events.eventid + ".png", "rb").read()).decode()
        eachEvent = {"eventid": events.eventid, "photo": photo_data, "content": events.recoged}
        return eachEvent
    else:
        raise AssertionError("Illegal data input!")
