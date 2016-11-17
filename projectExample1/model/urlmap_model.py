# coding: utf8

from sqlalchemy import Column, Integer, Numeric, String

from util.engine import ORMBase


class UrlMap(ORMBase):
    __tablename__ = 'tbl_urlmap'  # URL对应表
    id = Column(Integer, primary_key=True)
    key = Column(String(50), index=True)
    url = Column(String(300))

