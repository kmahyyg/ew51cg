#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#

import flask
from respmodel import *
from uuid import uuid4 as uuidgen
from dbop import *


def writeOrderData(orderjson):
    # TODO TO-BE-FINISHED
    pass


def check_payment(orderid):
    # TODO TO-BE-FINISHED
    pass


def process_gateway(req):
    # TODO: reserved for process payment gateway response
    if isinstance(req, flask.request):
        pass
    else:
        pass
