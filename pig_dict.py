import os


# 读文件夹获取项目名称列表
def pig_name_list_get():
    pig_list = []
    path = "opt/share/"
    dirs = os.listdir(path)
    for file in dirs:
        pig_list.append(file)
    return pig_list


# 根据项目名称获取名称文件夹下的索引文件 源数据 和 相似群文件
def file_get(pig_list):
    pig_file_dic = {}
    for pig_name in pig_list:
        # print(type(pig_name))
        dic = {pig_name: {}}
        dic[pig_name]['name'] = pig_name
        ori_file_dir = 'opt/data/' + pig_name + '/'
        share_file_dir = 'opt/share/' + pig_name + '/'
        for dirpath, dirnames, filenames in os.walk(ori_file_dir):
            for file in filenames:
                if os.path.splitext(file)[1] == '.txt':
                    dic[pig_name]['ori_file'] = os.path.join(dirpath, file)

        for dirpath, dirnames, filenames in os.walk(share_file_dir):
            for file in filenames:
                if os.path.splitext(file)[1] == '.ann':
                    dic[pig_name]['ann_file'] = os.path.join(dirpath, file)
                if os.path.splitext(file)[1] == '.jsonl':
                    dic[pig_name]['similars_file'] = os.path.join(dirpath, file)
        pig_file_dic.update(dic)
    print(pig_file_dic)
    return pig_file_dic


if __name__ == '__main__':
    pig_list = pig_name_list_get()  # 获取项目名称列表
    pigFile_dic = file_get(pig_list)  # 所有项目的所有文件（字典存储）
    # pigClass_list = pigClass_get(pig_list, pigFile_dic)
