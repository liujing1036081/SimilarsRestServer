import json
from find_similars_unit import embedd_load, annoy_load, ori_dataReader
import sys
import os

'''
输入批量问题文本（txt文本）,
输出近似文本群,
保存在json文件中.
使用方式：在命令行中 python find_similars_test.py  share/data/u_q_wh15m_qas_raw.txt share/data/wh_emb100.ann data/test.txt share/data/wh_test_similars.jsonl
'''

def get_nns_by_vector(annoy, questions, wh_lines, topk=10):  # questions 是测试数据，wh_lines 是源数据
    queries = set()
    avg = embedd_load()
    for i in range(len(questions)):
        # each sentence should be queried one time
        sent = questions[i]
        if sent in queries:
            continue
        if sent.startswith('http'):
            continue
        queries.add(sent)
        # remove duplicates in candidates
        sent_vec = avg(sent)
        items = annoy.get_nns_by_vector(sent_vec, topk)
        candidates = set(wh_lines[k] for k in items)
        # candidates.discard(sent)
        if len(candidates) < 1:
            continue
        yield sent, candidates


def save_similars(sentences, wh_lines, outfile, ann_file):  # 这里的sentences是测试数据
    # load ann index
    annoy = annoy_load(ann_file)
    # find similars and save
    with open(outfile, 'w') as fp:
        for sent, candidates in get_nns_by_vector(annoy, sentences, wh_lines):
            fp.write(json.dumps({
                'sent': sent,
                'similars': list(candidates)
            }) + '\n')


def main():
    try:
        # 获取 命令行中的输入 输出文件名
        oriData_file = sys.argv[1].strip()
        ann_file = sys.argv[2].strip()
        question_file = sys.argv[3].strip()
        similars_file = sys.argv[4].strip()
    except Exception as e:
        print('error:', e)

        me = os.path.basename(__file__)

        print('usage: %s<oriData> <ann_file> <question> <output>' % me)

        print('example: %s wh_data.txt wh_emb.ann test.txt out_similars.txt' % me)

        exit()
    # wanghong_corpus = 'share/data/u_q_wh15m_qas_raw.txt'  # 源数据路径
    # ann_file = 'share/data/wh_emb100.txt'  #  ann文件
    # test_corpus = 'data/test.txt'  # 测试数据路径
    # similars_file = 'share/data/wh_test_similars.jsonl' # 保存近似群文本

    wh_lines = ori_dataReader(oriData_file)  # 源数据
    sentences = ori_dataReader(question_file)  # 测试数据
    save_similars(sentences, wh_lines, similars_file, ann_file)
    print('近似群文件已生成!')


if __name__ == '__main__':
    main()
