# TODOlist

参考 https://github.com/lalor/todolist

> 顺便把原作者项目的TODO做了。😊

## 使用方法：

创建一个数据库 编码 `utf8mb4`

创建数据库表结构

类似这样

```sql
mysql -h127.0.0.1 -uroot -proot -Dtest -P3306 < todolist_test.sql
```

或者直接文件导入

修改 `app/setting.py` 配置 将对应的数据库连接参数修改正确

`pip install -r requirements.txt`

然后运行 `manage.py`

看到这样应该就是好了。

![](https://ws1.sinaimg.cn/large/ecb0a9c3gy1fz0fkjxw34j20zs0a2t9l.jpg)

![](https://ws1.sinaimg.cn/large/ecb0a9c3gy1fz0fkycl9aj22e81iyq9y.jpg)

## 涉及的一些东西(其实我是现学的🎸 轻喷谢谢)

-   一开始我用原作者的仓库克隆下来是运行不了的。搞了一会儿发觉搞不定，所以就索性自己搞。

### 目录结构

```
.
├── README.md
├── __pycache__
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   └── setting.cpython-36.pyc
│   ├── models.py
│   ├── setting.py
│   ├── static
│   │   ├── css
│   │   ├── fonts
│   │   └── js
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── modify.html
│   │   └── register.html
│   └── web
│       ├── __init__.py
│       ├── __pycache__
│       ├── forms.py
│       └── views.py
├── manage.py
├── requirements.txt
├── todolist_test.sql
```

### 模块、库

-   `Flask-Login`

    Flask-Login 为 Flask 提供了用户会话管理。它处理了日常的登入，登出并且长时间记住用户的会话。

    [文档](http://www.pythondoc.com/flask-login/)

    主要是用了 `login_required` 装饰器做登录权限控制

    ```python
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_app.login_manager._login_disabled:
                return func(*args, **kwargs)
            elif not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    ```

-   `Flask-SQLAlchemy`

    Flask-SQLAlchemy 是一个为您的 Flask 应用增加 SQLAlchemy 支持的扩展。它需要 SQLAlchemy 0.6 或者更高的版本。它致力于简化在 Flask 中 SQLAlchemy 的使用，提供了有用的默认值和额外的助手来更简单地完成常见任务。

    [文档](http://www.pythondoc.com/flask-sqlalchemy)

    SQLAlchemy 就是 orm 框架咯。

    Object-Relational Mapping，把关系数据库的表结构映射到对象上，所以就通过操作对象来进行数据库的增删改查。

-   `Flask-Bootstrap`

    Flask-Bootstrap 把 Bootstrap 打包进一个 扩展，这个扩展主要由一个叫“bootstrap”的蓝本（blueprint）组成。不过好久没有更新了，不支持 bootstrap 4 ，有时间可以搞一下 [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)。

    [Flask-Bootstrap Github 仓库地址](https://github.com/mbr/flask-bootstrap)
    
    建议看一下仓库里的静态文件 

    https://github.com/mbr/flask-bootstrap/blob/master/flask_bootstrap/templates/bootstrap/

-   `Flask-WTF`

    Flask-WTF 提供了简单地 WTForms 的集成。

-   `pymysql` -- mysql-connector 驱动

    PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库。

### 作为笔记吧。（我比较菜）

-   flask 的 Blueprint 蓝图注册

    官方文档

    A Blueprint is a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.

    通俗讲就是蓝图可以各个模块的视图函数写在不同的py文件当中。也不能这么说。就是不都是用 app.route() 这样子，例如我有一个模块 web,我注册了蓝图，然后我就可以用 web.route() 写视图函数。

    create:

    ```python
    from flask import Blueprint

    web = Blueprint("web", __name__)
    ```
    
    register:

    ```python
    from app.web import web

    app.register_blueprint(web)
    ```

-   Flask-SQLAlchemy 初始化以及操作

    ```python
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    db.create_all()
    # 看了源码才知道删除所有表是 drop_all()
    db.drop_all()
    ```

    ```python
    def create_all(self, bind='__all__', app=None):
        """Creates all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'create_all')

    def drop_all(self, bind='__all__', app=None):
        """Drops all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'drop_all')
    ```

-   导入配置文件

    ```python
    app = Flask(__name__)
    app.config.from_object('app.setting')
    # 引用 app.config["DEBUG"]
    ```

-   路由的写法

    最好是 /login/ 而不是 /login （👤个人觉得）

    - /login/

        如果路由写 /login/ 当你输入网址 /login 的时候会 301 重定向到 /login/

    -  /login

       如果路由写 /login 当你输入网址 /login/ 的时候会 404 Not Found

-   密码加密🔐

    ```python
    # 生成
    from werkzeug.security import generate_password_hash
    generate_password_hash(form.password.data)
    
    # 检查
    from werkzeug.security import check_password_hash
    check_password_hash(self.password, password)
    ```

-   端口、IP等写进配置文件

    ```python
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 9090
    ```

-   数据库连接 URL

    用的是 pymysql 驱动 所以 `mysql+pymysql`

    `mysql+pymysql://root:root@localhost:3306/todolist_test?charset=utf8mb4"`

## 最终效果

### register

![](https://ws1.sinaimg.cn/large/ecb0a9c3gy1fz0h0kl8hsj22e81iy102.jpg)

### login

![](https://ws1.sinaimg.cn/large/ecb0a9c3gy1fz0fkycl9aj22e81iyq9y.jpg)

### home page

![](https://ws1.sinaimg.cn/large/ecb0a9c3gy1fz0gzsp94ej22e81iythl.jpg)

## 总结

前端有点菜。后端不成熟。

还是要多加学习。⛽️