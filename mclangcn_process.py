import os
import openpyxl
import pickle


def lang_to_process(origin, processed="processed.lang",
                    path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", path_append=None,
                    origin_path=None):
    if path_append is not None:
        path = os.path.join(path, path_append)
    if origin_path is None:
        origin_path = path
    if not os.path.exists(path):
        os.makedirs(path)
    origin_path = os.path.join(origin_path, origin)
    process_path = os.path.join(path, processed)
    processed_line = []
    with open(origin_path, "r", encoding='utf-8') as f:
        line = f.readlines()
        f.close()
    for i in line:
        if "=" in i:
            i = i.replace("\t", "").replace("#", "[TAB]#", 1).replace("=", "[TAB]", 1).replace("[TAB]", "\t")
            processed_line.append(i)
        else:
            i = i.replace('\t', ' ')
            processed_line.append(i)
    with open(process_path, "w", encoding='utf-8') as f:
        f.writelines(processed_line)
        f.close()


def processed_to_list(path_o=r"D:\Users\Economy\git\Gitee\mclangcn-update\process", origin="mclangcn_origin.lang"):
    origin = os.path.join(path_o, origin)

    with open(origin, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lang_list = []
    for l in lines:
        l = l.split('\t')
        lang_list.append(l)
    return lang_list


def list_to_lang(lang_list, path_p=r"D:\Users\Economy\git\GitHub\mclangcn\texts", processed="zh_CN.lang"):
    processed = os.path.join(path_p, processed)
    lines = []
    with open(processed, 'w', encoding='utf-8') as f:
        for l in lang_list:
            if l[1] == '' and l[2] == '\n':
                line = l[0] + l[2]
            else:
                line = l[0] + '=' + l[1] + '\t' + l[2]
            lines.append(line)
        f.writelines(lines)


def processed_to_dict(lang_path, simple=False):
    add_dict = {}
    with open(lang_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for l in lines:
        if "++ b/text" in l:
            continue
        else:
            l = l.split('\t')
            if "##" in l[0] or l[0] in ['', ' ', '\n', ' \n']:
                continue
            elif simple:
                if '#' in l[1]:
                    print("文件有问题，正文出现注释！")
                    l[1] = l[1].split('#')[0]
                add_dict[l[0]] = l[1].replace('\n', '')
            else:
                if '#' not in l[2]:
                    print(l, "：未以#结尾，已自动添加")
                    l[2] = '#' + l[2]
                add_dict[l[0]] = [l[1], l[2]]
    return add_dict


def dict_to_lang(lang_dict, path=r"D:\Users\Economy\git\GitHub\mclangcn\texts", lang="zh_CN.lang"):
    lang = os.path.join(path, lang)
    lines = []
    with open(lang, 'w', encoding='utf-8') as f:
        for key in lang_dict:
            l = lang_dict[key]
            if l[0] == '' and l[1] == '\n':
                line = key + l[1]
            else:
                line = key + '=' + l[0] + '\t' + l[1]
            lines.append(line)
        f.writelines(lines)


def new_lang_list(add_dict, lang_dict, key_path):
    with open(key_path, 'r', encoding='utf-8') as f:
        keys = f.readlines()
    new_list = []
    for k in keys:
        key = k.replace("\n", '')
        if key in add_dict:
            value = add_dict[key][0]
            comment = add_dict[key][1]
            if comment == '#\n':
                try:
                    comment = lang_dict[key][1]
                except:
                    continue
        elif key in lang_dict:
            value = lang_dict[key][0]
            comment = lang_dict[key][1]
        else:
            if not ("##" in key or key in ['', ' ', '\n']):
                print("未找到", key, "的译文")
            value = ''
            comment = '\n'
        new_list.append([key, value, comment])
    return new_list


def lang_excel(lang_list, path=r"D:\Users\Economy\git\Gitee\mclangcn-update\process"):
    os.chdir(path)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    i = 1
    for lang in lang_list:
        sheet['A' + str(i)] = lang[0]
        sheet['B' + str(i)] = lang[1]
        sheet['c' + str(i)] = lang[2]
        i += 1
    workbook.save('1.xlsx')


# create_lang()
# list = read_lang_list()
# add_lang(0, 0, r"D:\Users\Economy\git\Gitee\mclangcn-update\add\add.lang")
def add_mclangcn():
    origin_path = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    path = r"D:\Users\Economy\git\Github\mclangcn-update"
    key_path = r"D:\Users\Economy\git\Gitee\MCBE-lang\other"
    add_path = os.path.join(path, 'add.lang')
    old_path = os.path.join(path, "processed.lang")
    with open(r"D:\Users\Economy\git\Gitee\MCBE-lang\object\Preview", 'rb+') as f:
        ver = pickle.load(f)
        f.close()
    version = str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "." + str(ver[3])
    key_name = version + '_onlykey.lang'
    new_key = os.path.join(key_path, key_name)
    lang_to_process('zh_CN.lang', "processed.lang", path=path, origin_path=origin_path)

    add = processed_to_dict(add_path)
    old = processed_to_dict(old_path)
    lang_list = new_lang_list(add, old, new_key)
    list_to_lang(lang_list)


# add_mclangcn()

