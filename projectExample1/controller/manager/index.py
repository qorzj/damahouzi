import json
import web

from controller.manager import clear

app = web.application()

app.add_mapping('/clear', clear.Clear)


def manager_wrapper(labor):
    ret = labor()
    if isinstance(ret, dict):
        ret['isManager'] = True
    return ret


app.add_processor(manager_wrapper)
