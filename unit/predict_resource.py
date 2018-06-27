#! -*- coding: utf-8 -*-
import json

import falcon

from unit.find_similars_unit import predict_similars


class predictResource(object):
    def __init__(self, pig_dic, avg):
        self.pig_dic = pig_dic
        self.avg = avg
    #     self.start_pig = start_pig

    def on_post(self, req, resp, pig_name):

        # pig_info_dic = start_handle.startHandle.pig_info_dic
        # avg = start_handle.startHandle.avg

        print('predicting.......')
        # 判断已经开启的服务和要执行的项目是否匹配
        # if pig_name in pig_info_dic.keys() and ('annoy' in pig_info_dic[pig_name].keys()):
        #     chunk = req.stream.read()
        #     if not chunk:
        #         print('请输入问句')
        #     sent_chunk = json.loads(chunk.decode('utf-8'))
        #     in_sent = sent_chunk['sent']
        #     sent_vecs = avg(in_sent)
        #     sent, candidates = predict_similars(pig_info_dic[pig_name]['annoy'],
        #                                         pig_info_dic[pig_name]['wh_lines'],
        #                                         in_sent, sent_vecs)

        if pig_name in self.pig_dic.keys() and ('annoy' in self.pig_dic[pig_name].keys()):
            chunk = req.stream.read()
            if not chunk:
                print('请输入问句')
            sent_chunk = json.loads(chunk.decode('utf-8'))
            in_sent = sent_chunk['sent']
            sent_vecs = self.avg(in_sent)
            candidates, cosine = predict_similars(self.pig_dic[pig_name]['annoy'],
                                                self.pig_dic[pig_name]['wh_lines'],
                                                sent_vecs)

            list_candtes = str(candidates[0])
            cosine_first = cosine[0]
            quote = {
                'sent': (
                    in_sent
                ),
                'candidates': list_candtes,
                'cosine': cosine_first

            }

            resp.status = falcon.HTTP_200
            resp.media = quote
            return resp
        else:
            print('项目不存在或者项目' + pig_name + '的服务未开启！')
