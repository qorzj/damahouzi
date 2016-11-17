# coding: utf8
import web
from web import ctx

from util import param
from model.urlmap_model import UrlMap


class Clear:
    def POST(self):
        ctx.db.query(UrlMap).delete()
        ctx.db.commit()
        return {"code": 0}
