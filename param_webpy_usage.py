import json
import param
import web

app = web.application()

user_info_data = {}
session_data = {}


def json_wrapper(labor):
    ret = labor()
    return json.dumps(ret)


app.add_processor(json_wrapper)


class Register:
    @param.input("username password:password declaration->declar?")
    def POST(self, username, password, declar):
        if username in user_info_data:
            return {"code": 1, "message": "username duplicated"}
        session_data[hash(username+password)] = username
        user_inf_data[username] = {"declaration": declar or ""}
        return {"code": 0}


app.add_mapping("/register", Register)


class Login:
    @param.input("name->username password:password")
    def POST(self, username, password):
        hash_code = hash(username+password)
        if hash_code not in session_data:
            return {"code": 1, "message": "username and password not matched"}
        web.setcookie("username", username)
        web.setcookie("token", hash_code)
        return {"code": 0}


app.add_mapping("/login", Login)


user_app = web.application()
app.add_mapping("/user", user_app)


def user_login_checker(labor):
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
    @param.input("$1->username")
    def GET(self, username):
        if web.ctx.username != username:
            return {"code": 1, "message": "access denied"}
        if username not in user_info_data:
            return {"code": 1, "message": "user not exist"}
        return {"code": 0, "data": user_info_data[username]}


user_app.add_mapping("/info/(.+)", UserInfo)


class UpdateInfo:
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
