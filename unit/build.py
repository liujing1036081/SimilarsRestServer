import json
from annoy import AnnoyIndex
from .pipeline import Pipeline, Reader, LineOps


class FileReader(Reader):

    def __init__(self, filename, batch_size=1, limit=-1):
        self.filename = filename
        self.batch_size = batch_size
        self.limit = limit

    def __iter__(self):
        with open(self.filename) as fp:
            lines = []
            count = 0
            for line in fp:
                lines.append(line)
                if len(lines) >= self.batch_size:
                    yield lines
                    lines = []
                count += 1
                if self.limit > 0 and count >= self.limit:
                    break
            if len(lines) > 0:
                yield lines


def get_question(sample):
    assert (isinstance(sample, dict))
    return sample['q']


import numpy as np


def parse_word_emb(line):
    items = line.strip().split()
    return (items[0], items[1:])


def map_word_emb(lines):
    embedding = {}
    for word, emb in lines:
        # skip first line
        if len(emb) < 10:
            continue
        embedding[word] = np.array(emb, dtype=np.float32)
    return embedding


def load_embedding(emb_file):
    emb_reader = FileReader(emb_file)
    emb_pipe = Pipeline(emb_reader, [parse_word_emb], writer=map_word_emb)
    emb_map = emb_pipe.run()
    print('embedding: ', len(emb_map))
    return emb_map


def filter_empty(batch):
    return [item for item in batch if item is not None]


class AvgTransformer:

    def __init__(self, embedding):
        self.embedding = embedding

    def __call__(self, sent):
        emb = []
        for ch in sent:
            if ch in self.embedding:
                emb.append(self.embedding[ch])
        if len(emb) > 0:
            return np.mean(np.array(emb), axis=0)
        return np.array([])


def build_annoy(vecs, outfile, dim=100):
    annoy = AnnoyIndex(dim)
    for i, v in enumerate(vecs):
        if v.shape[0] != dim:
            v = np.zeros(dim)
        annoy.add_item(i, v)

    annoy.build(10)
    annoy.save(outfile)


def get_nns_by_item(annoy, questions, topk=10):
    queries = set()
    for i in range(len(questions)):
        # each sentence should be queried one time
        sent = questions[i]
        if sent in queries:
            continue
        if sent.startswith('http'):
            continue
        queries.add(sent)
        # remove duplicates in candidates
        items = annoy.get_nns_by_item(i, topk)

        candidates = set(questions[k] for k in items)
        candidates.discard(sent)
        if len(candidates) < 1:
            continue
        yield sent, candidates


def save_similars(annoy_file, sentences, outfile):
    # load ann index
    annoy = AnnoyIndex(100)
    print('annoy:', annoy)
    annoy.load(annoy_file)
    # find similars and save
    with open(outfile, 'w') as fp:
        for sent, candidates in get_nns_by_item(annoy, sentences):
            fp.write(json.dumps({
                'sent': sent,
                'similars': list(candidates)
            }) + '\n')


# wh_reader = FileReader(wanghong_corpus, batch_size=100)
# wh_pipe = Pipeline(wh_reader, [LineOps.parse_json, get_question])  # json q a 模式
# wh_questions = wh_pipe.run()
# print(len(wh_questions))
# # print(avg('你好 怎么加的我？[微笑]'))
# avg_pipe = Pipeline([wh_questions], [avg])
# wh_vecs = avg_pipe.run()
# print('whPig vectors:', len(wh_vecs), len(wh_questions))
#
# print(len(wh_questions), wh_questions[:3])
# build_annoy(wh_vecs, 'share/data/wh_emb100.ann')
# # annoy = AnnoyIndex(100)
# # annoy.load('share/data/wh_emb100.ann')
# save_similars('share/data/wh_emb100.ann', wh_questions, 'share/data/wh_similars.jsonl')

# %time for sent, candidates in get_nns_by_item(annoy, wh_questions): pass
# 加载词向量,返回avg 能够得到单个句子的句向量
def embedd_load():
    embedding = load_embedding('opt/data/glove.6B.100d.txt')
    avg = AvgTransformer(embedding)
    return avg


# 加载annoy
def annoy_load(annoy_file):
    annoy = AnnoyIndex(100)
    # annoy_file = '../find_sent_similars/data/wh_emb100_test.ann'
    # annoy_file = 'share/data/wh_emb100.ann'
    annoy.load(annoy_file)
    return annoy


# 读取原始数据qa
def ori_dataReader_non_qa(filename):
    # 单句输入模式
    wh_reader = FileReader(filename, batch_size=100)
    wh_pipe = Pipeline(wh_reader, [LineOps.remove_tail_marks])  # 纯文本模式
    wh_lines = wh_pipe.run()
    return wh_lines


# 读取原始数据qa
def ori_dataReader_qa(filename):
    # 单句输入模式
    wh_reader = FileReader(filename, batch_size=100)
    wh_pipe = Pipeline(wh_reader, [LineOps.parse_json, get_question])  # qa文本模式
    wh_lines = wh_pipe.run()
    return wh_lines


def qa_mod(ori_filename, ann_file, similars_file):
    print('开始build。。。。')
    wh_lines = ori_dataReader_qa(ori_filename)
    # print(len(wh_lines), wh_lines[:3])
    avg = embedd_load()
    print('加载avg')
    line_avg = Pipeline([wh_lines], [avg])
    vecs = line_avg.run()
    print(len(vecs), len(wh_lines))
    build_annoy(vecs, ann_file)
    save_similars(ann_file, wh_lines,
                  similars_file)


# def non_qa_mod(ori_filename, ann_file, similars_file):


if __name__ == '__main__':
    ori_filename = './opt/data/yy/yy_wh_data.json'
    ann_file = './opt/share/yy/yy_wh_emb100.ann'
    similars_file = './opt/share/yy/yy_wh_similars.jsonl'
    # 生成索引文件和近似群文件
    print('开始build。。。。')

    # 源文件格式是q a模式的文件
    wh_lines = ori_dataReader_qa(ori_filename)

    # 源文件格式是非q a 模式的行文本
    # wh_lines = ori_dataReader_non_qa(ori_filename)

    # print(len(wh_lines), wh_lines[:3])
    avg = embedd_load()
    print('加载avg')
    wh_avg = Pipeline([wh_lines], [avg])
    wh_vecs = wh_avg.run()
    print(len(wh_vecs), len(wh_lines))
    build_annoy(wh_vecs, ann_file)
    save_similars(ann_file, wh_lines,
                  similars_file)
