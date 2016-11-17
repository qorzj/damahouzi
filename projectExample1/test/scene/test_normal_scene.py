import json

from index import app
from util import logger

LOG = logger.init_logger()


def test_normal_scene():
    parsec_url = 'http://www.parsec.com.cn'
    
    ret = app.request('/add', 'POST', {'url': parsec_url})
    LOG.info(ret)
    ret_data = json.loads(ret.data)
    assert ret_data['code'] == 0
    key = ret_data['key']
    
    ret = app.request('/_' + key)
    LOG.info(ret)
    assert ret.status == '303 See Other' and ret.headers['Location'] == parsec_url
    
    ret = app.request('/manager/clear', 'POST')
    ret_data = json.loads(ret.data)
    assert ret_data['code'] == 0
    
    ret = app.request('/_' + key)
    ret_data = json.loads(ret.data)
    assert ret_data['code'] == 1


def setup():
    from util.engine import ORMBase, engine as _db
    ORMBase.metadata.create_all(_db)


def teardown():
    from util.engine import ORMBase, engine as _db
    ORMBase.metadata.drop_all(_db)
