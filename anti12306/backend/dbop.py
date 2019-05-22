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
# Filename: dbop.py
#
from sqlalchemy import Column, String, create_engine, Boolean, Float, UniqueConstraint, CheckConstraint, or_, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import SMALLINT
from apikey import sqlconn
from time import time
from secrets import token_hex as tokengen

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    username = Column(String(20), primary_key=True, unique=True)
    password = Column(String(64), nullable=False)
    is_vip = Column(Integer, nullable=False, default=0)
    # is_vip, vip user badge(8), admin badge(9)
    # is_vip, normal user(0)
    balance = Column(Float, nullable=False, default=0.0)
    apikey = Column(String(64), nullable=False)
    break_law = Column(Integer, nullable=False, default=0)
    # salt should be generated using token_hex
    salt = Column(String(16), nullable=False, default=str(tokengen(8)))
    topup_amount = Column(Float, nullable=False, default=0.0)


class Session(Base):
    __tablename__ = 'sessions'
    username = Column(String(20), primary_key=True)
    usrtoken = Column(String(80), nullable=False)
    logged = Column(Integer, default=int(time()))
    UniqueConstraint('username', 'usrtoken', name='uka')


class Order(Base):
    __tablename__ = 'orders'
    orderid = Column(String(80), primary_key=True)
    username = Column(String(20), nullable=False)
    submitat = Column(Integer, default=int(time()))
    amount = Column(Float, nullable=False)
    gateway = Column(String(10), nullable=False, default='alipay')
    CheckConstraint(or_(gateway == 'alipay', gateway == 'py_pay'))
    status = Column(SMALLINT, nullable=False, default=1)
    # 1 = created, 0 = success, 2 = failed, 3 = fraud


class UploadEvent(Base):
    __tablename__ = 'upload'
    username = Column(String(20), nullable=False)
    eventid = Column(String(80), primary_key=True)
    chnchars = Column(Integer, nullable=False)
    recoged = Column(String(15), nullable=True)
    UniqueConstraint('username', 'eventid', name='ukb')
    upltime = Column(Integer, default=int(time()))
    status = Column(SMALLINT, nullable=False, default=0)


def create_db_conn():
    engine = create_engine(sqlconn, pool_pre_ping=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def db_exit(session):
    session.commit()
    session.close_all()
    return 0

#
# try:
#     dbsess.add(adatah)
#     dbsess.commit()
# except InvalidRequestError as e:
#     print(e)
#     dbsess.rollback()
#     dbsess.commit()
#
