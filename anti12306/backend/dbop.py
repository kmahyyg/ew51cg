#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

from sqlalchemy import Column, String, create_engine, Boolean, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from apikey import sqlconn

Base = declarative_base()

class userdbmsg(Base):
    # SQL_TABLE_DATA_STRUCTURE
    # ID = Primary, Auto_increment, INT(12), NOT OVERRIDE
    # ISGROUP = Boolean. If false, groupid = '0'
    # GROUPID,USERID = VARCHAR(20)
    # MESSAGE = VARCHAR(800)
    # TIMESTAMP = Current_Timestamp(6), TIMESTAMP(6), NOT OVERRIDE

    __tablename__ = 'qqchat'

    id = Column(Integer(), primary_key=True)
    isgroup = Column(Boolean())
    groupid = Column(String(20))
    userid = Column(String(20))
    message = Column(String(800))
    timestamp = Column(TIMESTAMP(6))


def create_db_conn():
    engine = create_engine(sqlconn, pool_pre_ping=True)
    DBSession = sessionmaker(bind=engine)
    ses3sion = DBSession()
    return ses3sion


def db_exit(session):
    session.commit()
    session.close_all()
    return 0


try:
    dbsess.add(adatah)
    dbsess.commit()
except InvalidRequestError as e:
    print(e)
    dbsess.rollback()
    dbsess.commit()