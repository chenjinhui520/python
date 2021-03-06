from reboot.common.dbutils import MySQLHelper


db = MySQLHelper()

# 登陆时验证用户名和密码
def vilidate_login(username, password):
    sql = 'select * from user where username=%s and password=md5(%s)'
    args = (username, password)
    count, rt_list = db.fetch_one(sql, args)
    if count == 1:
        return True
    else:
        return False


# 获取所有用户信息
def get_user():
    columns = ("id", "username", "password", "job", "age", "role_name")
    sql = 'select id,username,password,job,age,role_name from user,role where user.role = role.role_id'
    user_list = []
    count, rt_list = db.fetch_all(sql)
    for user in rt_list:
        user_list.append(dict(zip(columns, user)))
    return user_list


def vilidate_find(username, passwd, age, job, role_name):
    sql = "select username from user where username=%s"
    args = (username,)
    count, rt_list = db.fetch_one(sql, args)
    if not username:
        return False, u'用户名不能为空'
    if count != 0:
        return False, u'用户名已存在'
    if not passwd:
        return False, u'密码不能为空'
    if not age:
        return False, u'年龄不能为空'
    if not job:
        return False, u'职务不能为空'
    if not role_name:
        return False, u'必须选择角色'
    return True, ''

def vilidate_change_user_passwd(userid, username, original_passwd, new_passwd, new_repasswd):
    if not vilidate_login(username, original_passwd):
        return False, '原始密码错误.'
    if not get_user_by_id(userid):
        return False, '用户不存在.'
    if new_passwd != new_repasswd:
        return False, '2 次新密码不一致.'
    if len(new_passwd) < 6:
        return False, '用户密码不能小于6位.'
    return True, ''

def change_user_passwd(userid, user_passwd):
    sql = 'update user set password=md5(%s) where id=%s'
    args = (user_passwd, userid)
    count, rt_list = db.execute(sql, args=args)
    return count != 0


# 添加用户
def add_user(username, passwd, age, job, role_id):
    sql = 'insert into user(username,password,job,age,role) values(%s,md5(%s),%s,%s,%s)'
    args = (username, passwd, job, age, role_id)
    count, rt_list = db.execute(sql, args=args)
    return count


def user_delete(uid):
    sql = 'delete from user where id=%s' % uid
    count, rt_list = db.execute(sql)
    return count != 0


def get_user_by_id(uid):
    columns = ("id", "username", "password", "job", "age")
    sql = 'select * from user where id=%s'
    args = (uid,)
    user_list = []
    count, rt_list = db.fetch_one(sql, args=args)
    for user in rt_list:
        user_list.append(dict(zip(columns, user)))
    return user_list

def get_role_from_username(username):
    sql = 'select role from user where username=%s'
    args = (username, )
    count, rt_list = db.fetch_one(sql, args=args)
    return rt_list

def get_role_by_role_name(role_name):
    sql = 'select role_id from role where role_name=%s'
    args = (role_name, )
    count, rt_list = db.fetch_one(sql, args=args)
    return rt_list

def user_update(uid, age, job, role):
    sql = 'update user set job=%s,age=%s,role=%s where id=%s;'
    args = (job, age, role, uid)
    count, rt_list = db.execute(sql, args=args)
    return count


def get_accesslog(topn=10):
    columns = ("id", "ip", "url", "status", "count")
    sql = 'select * from accesslog limit %s'
    args = (topn,)
    accesslog_list = []
    count, rt_list = db.fetch_all(sql, args=args)
    for item in rt_list:
        accesslog_list.append(dict(zip(columns, item)))
    return accesslog_list


