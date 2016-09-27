# damahouzi
the easyest and pythonest web framework (extends webpy)
python的web实践：
* 安装开发环境
* param组件+web.py框架
* sqlAlchemy
* 消息队列
* log(日志)
* 代码质量工具

## 安装开发环境
编辑器：
https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=mac&code=PCC

安装oh-my-zsh, brew, pip:
* oh-my-zsh： https://github.com/robbyrussell/oh-my-zsh
* brew： http://brew.sh/index.html
* sudo easy_install pip

安装依赖库:
* sudo pip install web.py
* brew install mysql
* sudo pip install mysql-python
* sudo pip install sqlalchemy

验证sqlalchemy+mysql是否安装成功：
``` 
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqldb://name:password@ip/table', pool_recycle=3600) 
```

## param组件+web.py框架
```
import param
@param.input(param_define)
```
> param_define格式： input_arg_name->method_arg_name:type*

* input_arg_name: 前端请求或URL中的变量名。如果是URL中，则是$1, $2...
* method_arg_name: 方法定义中的参数名称。如果是前端请求则可以省略。
* type: 参数类型名称。不填则为默认的字符串类型。
* 星号: 没有星号代表必传参数，带星号代表非不传。如果带星号又没有传值，则变量值为None

参数类型名称除了"s"和"file"，都需要用param.set_valueof(type_name, valueof_func)来定义。
比如要实现自然数类型"n0"，方法如下：
```
def nature_int_valueof(s):
    n = web.intget(s, -1)
    if n >= 0:
        return n, None
    return None, {"code": 1, "message": "wrong format!"}

@param.set_valueof("n0", nature_int_valueof)
```
如果n0类型的参数解析失败，不论是否是必传参数，框架都会直接返回 {"code": 1, "message": "wrong format!", "errorField": input_arg_name}

## sqlAlchemy
* 讲解视频： https://www.youtube.com/watch?v=51RpDZKShiw
* 视频的文本记录： https://github.com/qorzj/damahouzi/blob/master/sqlalchemy_usage.py

## 消息队列
* 参考： http://python-rq.org/docs/

## log(日志)
```
import logging
def init_logging(path=''):
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(path) if path else logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #formatter = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("init logging done")
    return logger

logger = init_logging()
logger.info("hahaha")

#output of format 1:
# 2016-09-27 20:41:42,370 - {fname} - INFO - init logging done
# 2016-09-27 20:41:42,370 - {fname} - INFO - hahaha
#output of format 2:
# [logger.py:13 -         init_logging() ] init logging done
# [logger.py:17 -             <module>() ] hahaha
```

## 代码质量工具
google编码规范
* 参考： http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/

pygenie
* 作用： 计算代码圈复杂度
* 用法： pygenie all -v codepath
* 下载安装： https://github.com/mattvonrocketstein/pygenie

nosetests
* 安装： sudo pip install nose
* 参考： http://pythontesting.net/framework/nose/nose-introduction/
