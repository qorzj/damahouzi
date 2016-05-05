import re
def is_email(text):
    if re.match("^(\\w)+(\\.\\w+)*@(\\w)+((\\.\\w+)+)$", text):
        return True
    return False

input_param = \
    {'password': ('str', 
            "password is too short", lambda x:len(x)>=8,
            "password is too long", lambda x:len(x)<=64, 
        ),

    'old_password': ('str', 
            "old password is too long", lambda x:len(x)<=64, 
        ),

    'email': ('str', 
            "email format error", is_email,
        ),

    'name': ('str', 
            "true name length error", lambda x:2<=len(x)<=64,
        ),

    }
