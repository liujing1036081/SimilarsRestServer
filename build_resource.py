# import falcon
# from ann_generate import none_qa_mod
#
#
# class build_Resource():
#     def on_post(self, req, resp, pig_name):
#         if pig_name in pig_list:
#             if pig_name == 'whPig':
#                 ori_filename = whPig.ori_data
#                 ann_file = whPig.ann_file
#                 similars_file = whPig.similars_file
#                 none_qa_mod(ori_filename, ann_file, similars_file)
#                 print('.ann and similars file of pig whPig has been build!')
#
#         else:
#             print('there is no '+pig_name+' pig in pig_list!')
#         # raise falcon.HTTPGatewayTimeout()
#         resp.status = falcon.HTTP_200


