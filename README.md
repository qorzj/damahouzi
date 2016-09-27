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

## sqlAlchemy
* 讲解视频： https://www.youtube.com/watch?v=51RpDZKShiw
* 视频的文本记录： https://github.com/qorzj/damahouzi/blob/master/sqlalchemy_usage.py

## 代码质量工具
### google编码规范
* 参考： http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/

### pygenie
* 作用： 计算代码圈复杂度
* 用法： pygenie all -v codepath
* 下载安装： https://github.com/mattvonrocketstein/pygenie

### nosetests
* 安装： sudo pip install nose
* 参考： http://pythontesting.net/framework/nose/nose-introduction/
