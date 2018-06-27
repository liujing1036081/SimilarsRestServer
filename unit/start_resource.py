import falcon
# from app_start import pigFile_dic
# from config import pig_list
from unit.find_similars_unit import ann_load, ori_dataReader_qa
from unit.pig_dict import file_get, pig_name_list_get


class startResource(object):
    def __init__(self, pig_dic, avg):
        self.pig_dic = pig_dic
        self.avg = avg

        # self.__class__.pig_info_dic = self.pig_dic
        # self.__class__.avg = self.avg

    # def on_post(self, req, resp, pig_name):
    #     if pig_name in self.__class__.pig_info_dic.keys() and \
    #             ('annoy' not in self.__class__.pig_info_dic[pig_name].keys()):
    #         annoy_file = self.__class__.pig_info_dic[pig_name]['ann_file']
    #         ori_corpus = self.__class__.pig_info_dic[pig_name]['ori_file']
    #         self.__class__.pig_info_dic[pig_name]['annoy'] = ann_load(annoy_file)
    #         print('加载ann文件完成')
    #         self.__class__.pig_info_dic[pig_name]['wh_lines'] = ori_dataReader(ori_corpus)
    #         print('加载源数据完成')
    #         print('项目' + pig_name + '服务开启，可以进行单句预测')
    #     else:
    #         print('there is no' + pig_name + 'pig in pig_list')
    #         resp.status = falcon.HTTP_200

    def on_post(self, req, resp, pig_name):
        self.pig_dic = file_get(pig_name_list_get())

        if pig_name in self.pig_dic.keys() and \
                ('annoy' not in self.pig_dic[pig_name].keys()):
            annoy_file = self.pig_dic[pig_name]['ann_file']
            ori_corpus = self.pig_dic[pig_name]['ori_file']
            self.pig_dic[pig_name]['annoy'] = ann_load(annoy_file)
            print('加载ann文件完成')
            self.pig_dic[pig_name]['wh_lines'] = ori_dataReader_qa(ori_corpus)
            print('加载源数据完成')
            print('项目' + pig_name + '服务开启，可以进行单句预测')
        else:
            print('there is no' + pig_name + 'pig in pig_list')
            resp.status = falcon.HTTP_200

