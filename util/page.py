import web
import json
import re
import hashlib
import sqlite3
from util.param import input_param


render = web.template.render
end = None

def orm(col_csv, values):
    return web.utils.Storage(dict(zip(col_csv.split(','), values)))


def one(db_res):
    row = db_res.fetchone()
    if row:
        return row[0]
    return None


def pair_list(lst):
    i = 0
    for y in lst:
        i += 1
        if i & 1:
            x = y
        else:
            yield x, y
    end


def need_login(is_need):
    def f(g):
        def h(*a, **b):
            ck = web.cookies()
            web.ctx.conn = sqlite3.connect("data/data.db")
            token = ck.get('face', '!')
            cols = "id,email,fullname"
            row = web.ctx.conn.cursor().execute(
                    'select %s from member where member_id=?' % cols, (token,)).fetchone()
            me = dict(zip(cols.split(','), row)) if row else None
            if me is None and is_need:
                return web.seeother("/login", True)
            web.ctx.user = web.utils.Storage(me)
            return g(*a, **b)
        return h
    return f
        

def input(*params):
    def f(g):
        def h(*a, **b):
            it = web.input()
            for old_key in params:
                is_check, key = (False, old_key[1:]) if old_key and old_key[0] == '*' else (True, old_key)
                tipe = input_param[key][0]
                if tipe == 'int':
                    b[key] = web.utils.intget(it.get(key, ''), None)
                else:
                    b[key] = it.get(key, None)
                if is_check:
                    
                    for failmsg, f in pair_list(input_param[key][1:]):
                        if it[key] is None:
                            return ajax({'code':1, 'message':"%s is not given" % key})
                        if not f(it[key]):
                            return ajax({'code':1, 'message':failmsg})
            return g(*a, **b)
        return h
    return f


def passwd_hash(passwd):
    return hashlib.sha1(passwd).hexdigest()


