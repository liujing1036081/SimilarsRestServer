import json
import os

import falcon

import pymysql.cursors
import pymysql
import pandas as pd

from unit.build import qa_mod
from unit.config import ori_data_root, save_file_root
from unit.mk_dir import mkdir


class buildResource():
    def on_post(self, req, resp, pig_name):

        # 连接配置信息
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
        try:
            with con.cursor() as cursor:
                # sql = "select question as q , answer as a from simsent"
                print('项目名称是： ', pig_name)

                sql = "select question as q , answer as a from simsent where user_id =" \
                      " (select id from users  where username= %s)"
                cursor.execute(sql, pig_name)
                result = cursor.fetchall()
                # print(result)
        finally:
            con.close()
        if result == ():
            print('没有找到该项目的数据！！')
            return
        df = pd.DataFrame(result)  # 转换成DataFrame格式
        # print(df[:3])
        print('文本条数： ', df.count())  # 6767
        data_list = df.to_dict(orient='records')  # DataFrame 转换为dict组成的列表
        # 首先创建存储文件的文件夹
        # 数据库读取文件保存路径
        mkdir(ori_data_root + pig_name)
        # 生成的索引文件和similars文件的保存路径
        mkdir(save_file_root + pig_name)

        with open(os.path.join(ori_data_root + pig_name, pig_name + '.json'), 'w') as f:
            i = 0
            while True:
                try:
                    json.dump(data_list[i], f)
                    f.write('\n')
                    i += 1
                except IndexError:
                    break
        ori_filename = os.path.join(ori_data_root + pig_name, pig_name + '.json')
        ann_file = os.path.join(save_file_root + pig_name, pig_name + '_emb100.ann')
        similars_file = os.path.join(save_file_root + pig_name, pig_name + '_similars.json')
        # wh_lines = ori_dataReader_qa(ori_filename)

        qa_mod(ori_filename, ann_file, similars_file)

        resp.status = falcon.HTTP_200
