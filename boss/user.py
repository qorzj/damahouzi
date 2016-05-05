#coding: utf8
import web
import random
from util import page, config

urls = ("/register", "Register",
        "/login", "Login",
        "/list", "List",
        "/setting/password", "Password",
        )

app = web.application(urls, globals())
render = page.render('template', base='base')

class Register(object):
    @page.need_login(False)
    def GET(self):
        if web.ctx.user:
            return {'code':1, 'message':'already login'}
        return render.register()
        
    @page.need_login(False)
    @page.input('email', 'password', 'name')
    def POST(self, email, password, name):
        if web.ctx.user:
            return {'code':1, 'message':'already login'}
        conn = web.ctx.conn
        cursor = conn.cursor()
        if cursor.execute('select 1 from member where email=?', (email,)).fetchone():
            return {'code':1, 'message':'email is used by someone else'}
        password = page.passwd_hash(password)       
        sql = "insert into member (email, password, fullname, member_id, url_token, confirm_key) values(?,?,?,'','','')"
        cursor.execute(sql, (email, password, name))
        conn.commit()
        return {'code':0, 'message':'ok'}


class Login(object):
    @page.need_login(False)
    def GET(self):
        if web.ctx.user:
            return {'code':1, 'message':'already login'}
        return render.login()

    @page.need_login(False)
    @page.input('email', 'password')
    def POST(self, email, password):
        if web.ctx.user:
            return {'code':1, 'message':'already login'}
        password = page.passwd_hash(password)       
        conn = web.ctx.conn
        cursor = conn.cursor()
        uid = page.one(cursor.execute('select id from member where email=? and password=?', (email, password)))
        if not uid:
            return {'code':1, 'message':'email and password not match'}
        token = ''.join([chr(random.randint(ord('0'), ord('z'))) for i in xrange(40)]) 
        cursor.execute('update member set member_id=? where id=?', (token, uid))
        conn.commit()
        web.setcookie('face', token)
        return {'code':0, 'message':'ok'}


class Password(object):
    @page.need_login(True)
    def GET(self):
        return render.password()

    @page.need_login(True)
    @page.input("password", "old_password")
    def POST(self, password, old_password):
        password2 = web.input().get("password2", "")
        user = web.ctx.user
        conn = web.ctx.conn
        cursor = conn.cursor()
        res = cursor.execute('select id from member where id=? and password=?', 
                (user.id, page.passwd_hash(old_password))).fetchone()
        if not res:
            return {'code':1, 'message':'old password is wrong'}
        if password != password2:
            return {'code':1, 'message':'new passwords are different'}
        cursor.execute('update member set password=? where id=?', (page.passwd_hash(password), user.id))
        conn.commit()
        return {'code':0, 'message':'ok'}


class List(object):
    @page.need_login(True)
    def GET(self):
        cursor = web.ctx.conn.cursor()
        info = cursor.execute("select sql from sqlite_master where type = 'table' and name = 'member'").fetchone()[0]
        if config.is_logger_on:
            web.ctx.logger.info("test")
        cols = [x.split()[0] for x in info.split('(',1)[-1].rsplit(')',1)[0].split(',')]
        #rows = cursor.execute('select name from sqlite_master where type = "table"')
        rows = cursor.execute('select * from member')
        res = [dict(zip(cols, row)) for row in rows]
        return {'code':0, 'lst':res}


