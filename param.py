import web


def __str_valueof(s):
    return s, None


REFLECT_URL_MAP = {'s': __str_valueof}


def set_valueof(type_name, valueof_func):
    """
    usage:
    def postv_int_valueof(s):
        n = web.intget(s, 0)
        return (n, None) if n > 0 else (None, {"code": 1, "message": "wrong format"})

    param.set_valueof("n", postv_int_valueof)

    if parse failed, user will get {"code": 1, "message": "wrong format", "errorField": ??} as response
    """
    REFLECT_URL_MAP[type_name] = valueof_func


def input(param):
    """
    usage:
    @param.input("$1->uid:n? name->uname icon:file")
    def POST(self, uid, uname, icon):
        return {"data": [uid, uname, [icon.filename, icon.value, icon.file.read()]]}  #file contents Or use a file(-like) object
    """
    def f(g):
        def h(*a, **b):
            it = web.input()
            for param_unit in param.split():
                param_unit, is_optional = (param_unit[:-1], True) if param_unit[-1] == '?' else (param_unit, False)
                left_seg, val_type = param_unit.split(':', 1) if ':' in param_unit else (param_unit, 's')
                front_key, back_key = left_seg.split('->', 1) if '->' in left_seg else (left_seg, left_seg)
                if val_type == 'file':
                    file_it = web.input(**{front_key: {}})
                    real_val = file_it[front_key]
                    if not real_val:
                        if is_optional:
                            real_val = None
                        else:
                            return {'code': 1, 'isEmpty': True, 'errorField': front_key}
                    b[back_key] = real_val
                    continue
                real_val_str = a[int(front_key[1:])] if front_key[0] == '$' else it.get(front_key, None)
                if real_val_str is None:
                    real_val_str = ''
                if real_val_str == '':
                    if is_optional:
                        b[back_key] = None
                        continue
                    else:
                        return {'code': 1, 'isEmpty': True, 'errorField': front_key}
                real_val, error_json = REFLECT_URL_MAP[val_type](real_val_str)
                if error_json:
                    error_json['errorField'] = front_key
                    return error_json
                b[back_key] = real_val
            return g(a[0], **b)

        return h

    return f
