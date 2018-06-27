import pymysql.cursors
import pymysql
import pandas as pd

'''
用来查看数据库中的数据'''

config = {
    'host': '192.168.1.81',
    'port': 3306,  # MySQL默认端口
    'user': 'root',  # mysql默认用户名
    'password': 'admin',
    'db': 'chatCN',  # 数据库
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 创建连接
con = pymysql.connect(**config)
# 执行sql语句
# pig_name = '3284742556'
pig_name = '6119395091'



try:
    with con.cursor() as cursor:
        # sql = "select * from simsent"
        sql = "select username from users where id=280 "
        # sql = "select question as q , answer as a from simsent where user_id =" \
        #       " (select id from users  where username= %s)"

        cursor.execute(sql, pig_name)
        result = cursor.fetchall()

finally:
    con.close()
    print(result)
# df = pd.DataFrame(result)  # 转换成DataFrame格式
# print(df[:3])   # 6767
