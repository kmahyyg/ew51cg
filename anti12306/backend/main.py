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

from flask import Flask, jsonify, request
from uuid import uuid4 as uuidgen
from dbop import *

app = Flask(__name__)

@app.route('/api/user/login', methods=['POST'])
def userlog():
    usercreds_nm = request.form['username']
    usercreds_pw = request.form['password']
    usercreds_nm = request.form['_']


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
