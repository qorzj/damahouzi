import web


def binary_valueof(s):
    if s != '0' and s != '1':
        return None, {"code": 1, "message": "wrong format"}
    return int(s), None


def enum_valueof(s, restrict):
    """
    usage:
    enum : invalid (restrict is necessary)
    enum(4) : integer which value >= 0 and value <= 4
    enum(1-4) : integer which value >= 1 and value <= 4
    """
    p, q = restrict.split('-', 2) if '-' in restrict else ('0', restrict)
    start_num = web.intget(p, '-1')
    range_to_num = web.intget(q, '-1')
    if start_num < 0 or range_to_num < 0:
        return None, {"code": 1, "message": "inner setting error"}
    value = web.intget(s, None)
    if value is None:
        return None, {"code": 1, "message": "wrong format"}
    if not start_num <= value <= range_to_num:
        return None, {"code": 1, "message": "wrong range"}
    return value, None


def non_negtv_int_valueof(s):
    n = web.intget(s, 0)
    return (n, None) if n >= 0 else (None, {"code": 1, "message": "wrong format"})


def postv_int_valueof(s):
    n = web.intget(s, 0)
    return (n, None) if n > 0 else (None, {"code": 1, "message": "wrong format"})


def set_all():
    from util import param
    param.set_valueof('b', binary_valueof)
    param.set_valueof('enum', enum_valueof)
    param.set_valueof('n', postv_int_valueof)
    param.set_valueof('n0', non_negtv_int_valueof)
    