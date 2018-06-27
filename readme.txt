近似群获取服务
1. 单句相似句子的检索服务api是app_start.py
    启动服务器：
        gunicorn -b 127.0.0.1:8000 app


    服务使用示例：
        （a）:
        <start>：
        加载某项目的单句测试准备文件：.ann 和 similars文件
        访问方式： http POST localhost:8000/{pig_name}/start

        （b）：
        <predict>:
        单句测试调用接口：
        访问方式： http POST localhost:8000/{pig_name}/similars sent=主要播什么
        每次只输入一个句子，
        每次只返回一个近似度最高的句子和余弦值（命令行中能看到前十条近似度最高的句子和余弦值）

        （c）：
        <stop>:
        关闭某项目的单句测试的准备文件：.ann 和 similars文件
        访问方式： http POST localhost:8000/{pig_name}/

        (d):
        <build>:
        读取项目的原数据,生成索引文件 .ann和 similars文件
        访问方式：http POST localhost:8000/{pig_name}/build


2. 批量的近似群获取测试模块是find_similars_batch.py
    功能描述：
        输入批量测试文本,
        输出近似文本群,
        保存在json文件中.
        使用方式：在命令行中 python find_similars_test.py  share/data/u_q_wh15m_qas_raw.txt share/data/wh_emb100.ann data/test.txt share/data/wh_test_similars.jsonl

