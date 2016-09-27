# damahouzi
the easyest and pythonest web framework (extends webpy)
python的web实践：
* 安装开发环境
* param组件+web.py框架
* sqlAlchemy
* message-queue
* log(日志)
* 代码质量工具

## 安装开发环境
编辑器：
https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=mac&code=PCC

安装oh-my-zsh, brew, pip:
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
### nosetests
http://pythontesting.net/framework/nose/nose-introduction/
