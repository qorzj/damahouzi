from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#CREATE DATABASE ENGINE
engine = create_engine('mysql+mysqldb://name:password@ip/table', pool_recycle=3600)
engine = create_engine('sqlite:///:memory:')
engine.echo = True

#ESTABLISHING A SESSION
Session = sessionmaker(bind=engine)
session = Session()

#DEFINING MODELS
Base = declarative_base()
from sqlalchemy import Column, Integer, Numeric, String
class UserInfo(Base):
    __tablename__ = 'tbl_cookies'
    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

#PERSISTING OUR TABLE
Base.metadata.create_all(engine)  #表已存在则忽略，不会清空数据或改变表结构。可以用drop_all()删表。但无法ALTER表结构

#INSERT
##ADD A COOKIE
cc_cookie = Cookie(cookie_name='chip', cookie_recipe_url='http://some.me', cookie_sku='CC01', quantity=12, unit_cost=0.50)
session.add(cc_cookie)
session.commit()
print(cc_cookie.cookie_id)  #output: 1

## BULK SAVING
c1 = Cookie(...)
c2 = Cookie(...)
session.bulk_save_objects([c1, c2])
session.commit()
c1.cookie_id  #value: None

#QUERY
##ALL THE COOKIES
cookies = session.query(Cookie).all()
print(cookies)  #output:  [Cookie(cookie_name='chip',...), Cookie(...), Cookie(...)]

for cookie in session.query(Cookie):
    print(cookie)  #output: Cookie(...)

##PARTICULAR ATTRIBUTES
print(session.query(Cookie.cookie_name, Cookie.quantity).first())  #output: ('chip', 12)

##ORDER BY
for cookie in session.query(Cookie).order_by(Cookie.quantity):
    print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))  #output:  12 - chip

##DECENDING
from sqlalchemy import desc
for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
    print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))

##LIMITING
query = session.query(Cookie).order_by(Cookie.quantity).limit(2)
print([result.cookie_name for result in query])  #output: ['chip', 'butter']

##DATABASE FUNCTIONS
from sqlalchemy import func
inv_count = session.query(func.sum(Cookie.quantity)).scalar()  #scalar() get the first element whatever that happens to be assumed column
print(inv_count)  #output: 136

rec_count = session.query(func.count(Cookie.cookie_name)).first()
print(rec_count)  #output: (3, 0)

##LABELING
rec_count = session.query(func.count(Cookie.cookie_name).label('inventory_count')).first()
print(rec_count.keys())  #output: ['inventory_count']
print(rec_count.inventory_count)  #output: 3

##FILTER_BY
record = session.query(Cookie).filter_by(cookie_name = 'chip').first()
print(record)  #output: Cookie(cookie_name="chip",...)
record = session.query(Cookie).filter_by(Cookie.cookie_name == 'chip').first()

#CLAUSEELEMENTS
query = session.query(Cookie).filter(Cookie.cookie_name.like('%chip%'))

##CLAUSEELEMENTS METHODS
* between(cleft, cright) - Find where the column is between cleft and cright
* distinct() - Find only unique values for column* in_([list]) - Find where the column is in the list
* is_(None) - Find where the column is None (commonly used for Null checks with None)
* contains('string') - Find where the column has 'string' in it (Case-sensitve)
* endswith('string')
* startswith('string')
* ilike('string') - Find where the column is link 'string'

##OPERATORS
from sqlalchemy import cast
query = session.query(Cookie.cookie_name,
    cast(
        (Cookie.quantity * Cookie.unit_cost), Numeric(12,2)
    ).label('inv_cost'))
for result in query:
    print('{} - {}'.format(result.cookie_name, result.inv_cost))  #output: chip - 6.00

##CONJUNCTIONS
from sqlalchemy import and_, or_, not_
query = session.query(Cookie).filter(
    or_(
        Cookie.quantity.between(10, 50),
        Cookie.cookie_name.conteains('chip')
    )
)

#UPDATE
query = session.query(Cookie)
cc_cookie = query.filter(Cookie.cookie_name == "chip").first()
cc_cookie.quantity = cc_cookie.quantity + 120
session.commit()
print(cc_cookie.quantity)  #output: 132

#DELETE
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "butter")

dcc_cookie = query.one()
session.delete(dcc_cookie)
session.commit()
dcc_cookie = query.first()
print(dcc_cookie)  #output: None

#RELATIONSHIPS
##IMPORTS
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

##USER MODEL
class User(Base):
    __tablename__ = 'tbl_users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=??)

##ORDER MODEL
class Order(Base):
    __tablename__ = 'tbl_orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Intger(), ForeignKey('tbl_users.user_id'))
    shipped = Column(Boolean(), default=False)
    user = relationship("User", backref=backref('tbl_orders', order_by=??))

##LINEITEM MODEL
class LineItem(Base):
    __tablename__ = 'tbl_line_items'
    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('tbl_orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('tbl_cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))
    order = relationship("Order", backref=backref('tbl_line_items', order_by=??))
    cookie = relationship("Cookie", uselist=False)

##PERSIST THEM
Base.metadata.create_all(engine)

##DEFINING A USER
cookiemon = User(username='cookiemon', phone='111-1111', ...)
session.add(Cookiemon)
session.commit()

##SETTING UP AN ORDER
o1 = Order()
o1.user = cookiemon
session.add(o1)

##PREPARING LINE ITEMS
cc = session.query(Cookie).filter(Cookie.cookie_name == 'chip').one()
line1 = LineItem(cookie=cc, quantity=2, extended_cost=1.00)

pb = session.query(Cookie).filter(Cookie.cookie_name == 'raisin').one()
line2 = LineItem(quantity=12, extended_cost=3.00)
line2.cookie = pb

##ASSOCIATE ORDER AND LINE ITEMS
o1.line_items.append(line1)
o1.line_items.append(line2)
session.commit()

##USING RELATIONSHIPS IN QUERIES
query = session.query(Order.order_id, User.username, User.phone, Cookie.cookie_name, LineItem.quantity, LineItem.extended_cost)
query = query.join(User).join(LineItem).join(Cookie)
results = query.filter(User.username == 'cookiemon').all()
print(results)  #output: [(1, 'cookiemon', '111-1111', 'chip', ...), (1, 'cookiemon', '111-1111', 'raisin', ...)]

##ANOTHER EXAMPLE
query = session.query(User.username, func.count(Order.order_id))
query = query.outerjoin(Order).group_by(User.username)
for row in query:
    print(row)  #output: ('cookiemon', 1)

#EXECUTE SQL
result = session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})
for row in result:
    print row  #output: (493L, '\xe5\xbc\xa0\xe9\xb9\x8f\xe4\xb8\xbe', '13880775240', 11L, '\xe5\xb7\x9dA824EX', 0L, 1)

##JOIN WITHOUT RELATIONSHIP
class UserInfo(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    lpn = Column(String(45))

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    companyName = Column(String(50))

query = session.query(UserInfo.id, UserInfo.lpn, Company.companyName).join(Company, UserInfo.id==Company.id)
for row in query:
    print row[0], row[1], row[2]

#sql: SELECT user.id AS user_id, user.lpn AS use_lpn, company.`companyName` AS `company_companyName` FROM user INNER JOIN company ON user.id = company.id
#output: 
# 1 川A12345 平安
# 2 川A77777 人保
#注意: .query()中出现的第一个表名为主查询表，所以.join()第一个参数应该为副查询表，否则会执行出错
