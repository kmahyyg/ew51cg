#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#

import flask
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
        if (order_payment != 'py-pay') or (order_payment != 'alipay'):
            return None
        else:
            new_order = Order(username=order_nm, amount=order_amount,
                              orderid=str(uuidgen()),
                              gateway=order_payment)
            try:
                db_session.add(new_order)
                db_session.commit()
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
