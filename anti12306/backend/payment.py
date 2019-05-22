#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
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
# Filename: payment.py
#

from respmodel import *
from uuid import uuid4 as uuidgen
from dbop import *

global db_session
db_session = create_db_conn()


def event_num2desc(status_code):
    if isinstance(status_code, int):
        if status_code == 0:
            return "success"
        elif status_code == 1:
            return "created"
        elif status_code == 2:
            return "failed"
        elif status_code == 3:
            return "fraud"
        elif status_code == 4:
            return "waiting_for_manual_review"
        else:
            return "unknown"
    else:
        return None


def writeOrderData(orderjson):
    # if done, return orderid string
    # else return None
    try:
        order_nm = orderjson['username']
        order_amount = float(orderjson['amount'])
        order_payment = orderjson['payment']
        if (order_payment != 'py_pay') and (order_payment != 'alipay'):
            return None
        else:
            new_order = Order(username=order_nm, amount=order_amount,
                              orderid=str(uuidgen()),
                              gateway=order_payment)
            try:
                db_session.add(new_order)
                db_session.commit()
                return new_order.orderid
            except:
                db_session.rollback()
                db_session.commit()
    except:
        return None


def check_payment(orderid):
    try:
        orderobj = db_session.query(Order).filter_by(orderid=orderid).one()
        if isinstance(orderobj, Order):
            # the payment amount will automatically add to your balance by using database trigger.
            return afterPayResponse(
                orderid=orderobj.orderid,
                timestamp=int(orderobj.submitat),
                amount=float(orderobj.amount),
                resp=event_num2desc(orderobj.status)
            )
        else:
            raise UnboundLocalError("Will be handled by the program.")
    except:
        return errResponse(-1, "Invalid data.")


def process_gateway(req):
    # TODO: reserved for process payment gateway response
    # this response must be saved to another table which used to check the corresponding
    # relationship between internal order id and payment gateway order id
    # also, the response must change the order status in the database
    pass
