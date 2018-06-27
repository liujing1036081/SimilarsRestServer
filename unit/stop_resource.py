#! -*- coding: utf-8 -*-

import falcon
import gc


class stopResource(object):
    def __init__(self, pig_dic, avg):
        self.pig_dic = pig_dic
        self.avg = avg

    def on_post(self, req, resp, pig_name):
        if pig_name in self.pig_dic.keys() and \
                ('annoy' in self.pig_dic[pig_name].keys()):
            del self.pig_dic[pig_name]['annoy'], self.pig_dic[pig_name]['wh_lines']
            gc.collect()

            print('关闭项目' + pig_name + '服务成功！')
        else:
            print('there is no' + pig_name + 'pig in pig_list or this server has already been shut down!')
            resp.status = falcon.HTTP_200
