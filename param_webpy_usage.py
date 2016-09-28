#coding: utf8
import json
import param
import web


app = web.application()  #全局路由

user_info_data = {}
session_data = {}


def password_valueof(s):
    """
    解析密码的函数
    """
    if not 6 <= len(s) <= 128:
        return None, {"code": 1, "message": "invalid password length"}
    return s, None


param.set_valueof("password", password_valueof)


def json_wrapper(labor):
    """
    全局拦截器。作用1：支持跨域访问；作用2：把labor返回的dict对象转成json_str
    """
    ret = labor()
    web.header('Access-Control-Allow-Origin', '*')
    return json.dumps(ret)


app.add_processor(json_wrapper)


class Register:
    """
    用户注册
    """
    @param.input("username password:password declaration->declar?")
    def POST(self, username, password, declar):
        if username in user_info_data:
            return {"code": 1, "message": "username duplicated"}
        session_data[hash(username+password)] = username
        user_inf_data[username] = {"declaration": declar or ""}
        return {"code": 0}


app.add_mapping("/register", Register)


class Login:
    """
    用户登录
    """
    @param.input("name->username password:password")
    def POST(self, username, password):
        hash_code = hash(username+password)
        if hash_code not in session_data:
            return {"code": 1, "message": "username and password not matched"}
        web.setcookie("username", username)
        web.setcookie("token", hash_code)
        return {"code": 0}


app.add_mapping("/login", Login)


user_app = web.application()  #/user路径的路由
app.add_mapping("/user", user_app)


def user_login_checker(labor):
    """
    /user范围的拦截器。作用：判断用户是否已经登录
    """
    ck = web.cookies()
    ck_token = ck.get("token")
    ck_username = ck.get("username")
    username = session_data.get(ck_token, '')
    if not username or username != ck_username:
        return {"code": 1, "message": "need login"}
    web.ctx.username = username
    return labor()


user_app.add_processor(user_login_checker)


class UserInfo:
    """
    获取用户信息
    """
    @param.input("$1->username")
    def GET(self, username):
        if web.ctx.username != username:
            return {"code": 1, "message": "access denied"}
        if username not in user_info_data:
            return {"code": 1, "message": "user not exist"}
        return {"code": 0, "data": user_info_data[username]}


user_app.add_mapping("/info/(.+)", UserInfo)


class UpdateInfo:
    """
    更新用户信息
    """
    @param.input("username, declaration?")
    def POST(self, username, declaration):
        if web.ctx.username != username:
            return {"code": 1, "message": "access denied"}
        if username not in user_info_data:
            return {"code": 1, "message": "user not exist"}
        if declaration is not None:
            user_info_data[username]["declaration"] = declaration
        return {"code": 0}


user_app.add_mapping("/update", UpdateInfo)


if __name__ == "__main__":
    app.run()
