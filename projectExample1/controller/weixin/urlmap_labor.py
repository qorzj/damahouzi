# coding: utf8
import web
from web import ctx

from util import param
from model.urlmap_model import UrlMap
from sqlalchemy import func


class Add:
    @param.input("url")
    def POST(self, url):
        chrtbl = "0123456789" + (lambda s: s+s.upper())(
                "abcdefghijklmnopqrstuvwxyz")
        ntos = lambda x: chrtbl[x] if x < 62 else ntos(x / 62) + chrtbl[x % 62]
        cnt = ctx.db.query(func.count(UrlMap.id)).scalar()
        key = ntos(cnt * 1111 + hash(url) % 1111)
        data = UrlMap(key=key, url=url)
        ctx.db.add(data)
        ctx.db.commit()
        return {"code": 0, "key": key}


class Goto:
    @param.input("$1->key")
    def GET(self, key):
        data = ctx.db.query(UrlMap).filter_by(key=key).first()
        if not data:
            return {"code": 1, "message": "url not found"}
        web.seeother(data.url)
        return {"code": 0}
