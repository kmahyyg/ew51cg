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
# Filename: bankcomm.py

from base64 import b64decode
import shutil
import subprocess
import os


def comm_tensor(eventid):
    try:
        if shutil.which("calamari-predict") is None:
            raise ModuleNotFoundError
        else:
            pass
    except ModuleNotFoundError:
        dataresult = ("内部错误1", 4)
        return dataresult
    # Open models
    model_path = os.getcwd() + "/trained_models/model_current.ckpt"
    usrimgfn = os.getcwd() + "/userimgs/" + eventid + ".jpg"
    runstr = "calamari-predict --checkpoint " + model_path + " --files " + usrimgfn
    try:
        cpproc = subprocess.run(runstr, timeout=10)
        if cpproc.returncode != 0:
            dataresult = ("内部错误2", 4)
            return dataresult
        else:
            # Communicate with tensorflow backend, return Tuple(CHN char result, len(CHN))
            usrOCRfd = os.getcwd() + "/userimgs/" + eventid + ".pred.txt"
            usrocrreslt = open(usrOCRfd, 'r').read()
            dataresult = (usrocrreslt, len(usrocrreslt))
            return dataresult
    except:
        dataresult = ("内部错误3", 4)
        return dataresult


def save_photo(photoObj, eventid):
    fileloc = os.getcwd() + '/userimgs/' + eventid + '.jpg'
    photoObj.save(fileloc)
    return 0
