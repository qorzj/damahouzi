# coding: utf8
import json
import web

from util import engine, logger, valueof
from controller.manager import index as manager_index
from controller.weixin import urlmap_labor

valueof.set_all()


def global_wrapper(labor):
    """
    wrapper: logger, database, json
    """
    web.ctx.log = logger.init_logger()
    web.ctx.db = engine.Session()
    try:
        ret = labor()
    finally:
        web.ctx.db.close()
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')
    return json.dumps(ret, cls=engine.AlchemyEncoder)


app = web.application()
app.add_processor(global_wrapper)


app.add_mapping('/manager', manager_index.app)
app.add_mapping('/add', urlmap_labor.Add)
app.add_mapping('/_(.+)', urlmap_labor.Goto)


application = app.wsgifunc()


if __name__ == "__main__":
    engine.ORMBase.metadata.create_all(engine.engine)
    app.run()
