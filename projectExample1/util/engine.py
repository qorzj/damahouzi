import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import web

engine = create_engine('sqlite:///data.db')
engine.echo = True
Session = sessionmaker(bind=engine)
ORMBase = declarative_base()


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            field_dct = obj.__dict__.copy()
            field_dct.pop('_sa_instance_state', None)
            return field_dct

        return json.JSONEncoder.default(self, obj)


def orm_zip(keys, row_tuple):
    """
    orm_zip('id, name', (3, 'parsec')) => web.Storage(id=3, name='parsec')
    orm_zip(['user', 'pay.price'], (<ORMBase Object>, 64.5))
        => web.Storage{'user':{'id':3, 'name':'parsec'}, 'pay.price':64.5}
    """
    if isinstance(keys, str): keys = keys.replace(',', ' ').split()
    obj = web.Storage()
    for key, value in zip(keys, row_tuple):
        if isinstance(value.__class__, DeclarativeMeta):
            field_dct = value.__dict__.copy()
            field_dct.pop('_sa_instance_state', None)
            obj[key] = field_dct
        else:
            obj[key] = value
    return obj

