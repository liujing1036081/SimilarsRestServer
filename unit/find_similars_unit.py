import numpy
from annoy import AnnoyIndex

from unit.config import embedd_file
from .pipeline import Pipeline, Reader, LineOps
import numpy as np


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


def parse_word_emb(line):
    items = line.strip().split()
    return items[0], items[1:]


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


# cosine距离计算
def cosin_fun(vec1, vec2):
    num = float(numpy.sum(vec1 * vec2))
    denom = numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2)
    cos = num / denom
    return cos


def get_nns_by_vector(annoy, questions, sent_vec, topk):
    items = annoy.get_nns_by_vector(sent_vec, topk)
    # 计算in_sent和候选近似群之间的近似度（cosine距离）
    candidates_dict = {}
    for index in items:
        candidates_dict[index] = cosin_fun(sent_vec, annoy.get_item_vector(index))
    # 根据cosine近似度进行倒序排序,得到列表元祖(index, cosine_value)
    candidates_list = sorted(candidates_dict.items(), key=lambda d: d[1], reverse=True)
    candidates = list(questions[k[0]] for k in candidates_list)
    cosine = list(k[1] for k in candidates_list)
    yield candidates, cosine


def predict_similars(annoy, sentences, sent_vec):
    for candidates, cosine in get_nns_by_vector(annoy, sentences, sent_vec, topk=10):
        print('检索得到的近似句和对应的余弦值： ')
        for i in range(len(candidates)):
            print(candidates[i], cosine[i])
        return candidates, cosine


def embedd_load():
    embedding = load_embedding(embedd_file)
    avg = AvgTransformer(embedding)
    return avg


def ann_load(annoy_file):
    annoy = AnnoyIndex(100)
    annoy.load(annoy_file)
    return annoy


# 读取检索近似群的json数据
def ori_dataReader_non_qa(filename):
    wh_reader = FileReader(filename, batch_size=100)
    wh_pipe = Pipeline(wh_reader, [LineOps.remove_tail_marks])  # 纯文本模式
    wh_lines = wh_pipe.run()
    return wh_lines

def ori_dataReader_qa(filename):
    wh_reader = FileReader(filename, batch_size=100)
    wh_pipe = Pipeline(wh_reader, [LineOps.parse_json, get_question])  # qa文本模式
    wh_lines = wh_pipe.run()
    return wh_lines

