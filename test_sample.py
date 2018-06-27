"""
单元测试

yy项目用来做测试专用的 原数据文件有两百条文本
"""
from .unit.build import ori_dataReader_qa
from .unit.find_similars_unit import ann_load, ori_dataReader_qa, embedd_load, cosin_fun

yy_annoy = ann_load('./opt/share/yy/yy_wh_emb100.ann')
avg = embedd_load()

yy_ori_filename = './opt/data/yy/yy_wh_data.json'
wh_lines = ori_dataReader_qa(yy_ori_filename)


# 计算余弦相似度, 检测两个句向量shape是否相同，检测余弦值大小是否合理
def test_cosin_fun():
    sent1 = '哈哈，你好阿'
    sent2 = '你从哪里来艾我的朋友'
    vec1 = avg(sent1)
    vec2 = avg(sent2)
    assert vec1.shape == vec2.shape
    assert 0 <= cosin_fun(vec1, vec2) <= 1


# 检测相同的句子之间的cosine值是否为1(约等于1)
def test_cosin_func_2():
    sent1 = '哈哈，你好阿'
    sent2 = '哈哈，你好阿'
    vec1 = avg(sent1)
    vec2 = avg(sent2)
    assert 0.999 <= cosin_fun(vec1, vec2) <= 1.001


# 检测索引文件中的索引数与原文件中的数量是否相同
def test_build_annoy():
    # yy_annoy.get_n_items()  是索引文件中的索引个数
    assert len(wh_lines) == yy_annoy.get_n_items()

# 读取数据库数据，写入ori_filename 文件中的文本条数和数据库中读取的文件条数相同
# def test_db_read():
