近似群获取服务
1. 单句相似句子的检索服务api是app_start.py
    具体描述：
        （a）:
            '''
        <start>：
        加载某项目的单句测试的准备文件：.ann 和 源数据
        访问方式： http POST localhost:8000/{pig_name}/start
        '''
        （b）：
                '''
        <predict>:
        单句测试调用接口：
        访问方式： http POST localhost:8000/{pig_name}/similars sent=主要播什么
        每次只输入一个句子，
        每次只返回一个近似度最高的句子和近似值（命令行中能看到前十条）'''

2. 批量的近似群获取测试模块是find_similars_test.py
    具体描述：
            '''
        输入批量问题文本（txt文本）,
        输出近似文本群,
        保存在json文件中.
        使用方式：在命令行中 python find_similars_test.py  share/data/u_q_wh15m_qas_raw.txt share/data/wh_emb100.ann data/test.txt share/data/wh_test_similars.jsonl
        '''
