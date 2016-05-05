#coding: utf8
import web
import logging
import json
from util import page, config
from boss import user

def init_logging(path):
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(path)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("init logging done")
    return logger

urls = ("", user.app,
        )

app = web.application(urls, globals())

def load_logger(handler):
    if config.is_logger_on:
        web.ctx.logger = init_logging(config.log_filename)
    res = handler()
    if type(res) == dict:
        return json.dumps(res)
    elif res is None:
        return ''
    else:
        return res

app.add_processor(load_logger)

if __name__ == "__main__":
    app.run()
