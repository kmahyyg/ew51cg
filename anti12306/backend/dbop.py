#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

from sqlalchemy import Column, String, create_engine, Boolean, Float, UniqueConstraint, CheckConstraint, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP, SMALLINT
from apikey import sqlconn
from time import time

Base = declarative_base()


class User(Base):
    # SQL_TABLE_DATA_STRUCTURE

    __tablename__ = 'users'

    username = Column(String(20), primary_key=True)
    password = Column(String(64), nullable=False)
    is_vip = Column(Boolean, nullable=False, default=False)
    balance = Column(Float, nullable=False, default=0.0)
    apikey = Column(String(64), nullable=False)
    break_law = Column(Boolean, nullable=False, default=False)
    salt = Column(String(16), nullable=False)
    total_topup = Column(Float, nullable=False, default=0.0)


class Session(Base):
    __tablename__ = 'sessions'
    username = Column(String(20), primary_key=True)
    usrtoken = Column(String(80), nullable=False)
    logged = Column(TIMESTAMP, default=int(time()), nullable=False)
    UniqueConstraint('username', 'usrtoken', name='uka')


class Order(Base):
    __tablename__ = 'orders'
    orderid = Column(String(80), primary_key=True)
    username = Column(String(20), nullable=False)
    submitat = Column(TIMESTAMP, nullable=False, default=int(time()))
    amount = Column(Float, nullable=False)
    gateway = Column(String(10), nullable=False, default='alipay')
    CheckConstraint(or_(gateway == 'alipay', gateway == 'py_pay'))
    status = Column(SMALLINT(1), nullable=False, default=1)
    # 1 = created, 0 = success, 2 = failed, 3 = fraud


def create_db_conn():
    engine = create_engine(sqlconn, pool_pre_ping=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def db_exit(session):
    session.commit()
    session.close_all()
    return 0


# try:
#     dbsess.add(adatah)
#     dbsess.commit()
# except InvalidRequestError as e:
#     print(e)
#     dbsess.rollback()
#     dbsess.commit()
#
