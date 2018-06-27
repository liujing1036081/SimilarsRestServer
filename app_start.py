import falcon

from unit import build_resource, stop_resource, predict_resource, start_resource
from unit.find_similars_unit import embedd_load
from unit.pig_dict import file_get, pig_name_list_get

api = application = falcon.API()

# 获取项目字典
# pig_dic = file_get(pig_name_list_get())
pig_dic = {}

# 加载词向量
avg = embedd_load()

'''
<start>：
加载某项目的单句测试的准备文件：.ann 和 源数据
访问方式： http POST localhost:8000/{pig_name}/start  
'''

start = start_resource.startResource(pig_dic, avg)
api.add_route('/{pig_name}/start', start)


'''
<predict>:
单句测试调用接口：
访问方式： http POST localhost:8000/{pig_name}/similars sent=主要播什么
每次只输入一个句子，
每次只返回一个近似度最高的句子和近似值（命令行中能看到前十条）'''

predict = predict_resource.predictResource(pig_dic, avg)
api.add_route('/{pig_name}/predict', predict)


'''
<stop>:
关闭某项目的单句测试的准备文件：.ann 和 源数据
访问方式： http POST localhost:8000/{pig_name}/stop
'''

stop = stop_resource.stopResource(pig_dic, avg)
api.add_route('/{pig_name}/stop', stop)

'''
<build>:
读取项目的源数据,构建索引文件.ann和近似群文件
访问方式：http POST localhost:8000/{pig_name}/build'''
build = build_resource.buildResource()
api.add_route('/{pig_name}/build', build)
