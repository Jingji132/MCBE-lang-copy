import json
import os
import zipfile
from Update_Lang import read_info, version
from crowdin import download_translate


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


def process_zh_json():
    path = r"D:\Users\Economy\git\GitHub\test2\processed.lang"
    path1 = r"D:\Users\Economy\git\Gitee\lang-crowdin\en\processed.json"
    path2 = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    path3 = r"D:\Users\Economy\git\Gitee\lang-crowdin\en"

    lang_to_process('zh_CN.lang', origin_path=path2, path=path3)
    with open(path1, 'w+', encoding='utf-8') as f:
        json.dump(processed_to_dict(path, True), f, ensure_ascii=False)


def process_en_json(process, path=r"D:\Users\Economy\git\Gitee\MCBE-lang", path_append=None,
                    json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\processed.json"):
    if path_append is not None:
        path = os.path.join(path, path_append, process)
    else:
        path = os.path.join(path, process)

    with open(json_path, 'w+', encoding='utf-8') as f:
        json.dump(processed_to_dict(path, True), f, ensure_ascii=False)


def json_to_lang(json_path, lang_path, template):
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = json.load(f)
    with open(template, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lang = []
    for l in lines:
        list = l.split('\t')
        if '#' in list[0]:
            lang.append(l)
            continue
        elif list[0] in lang_dict:
            list[1] = lang_dict[list[0]]
            if len(list) == 2:
                lzh = list[0] + '=' + list[1] + '\t#\n'
            elif len(list) == 3:
                lzh = list[0] + '=' + list[1] + '\t#' + list[2]
            else:
                print("出错：" + list[0])
                lzh = l
            lang.append(lzh)
        else:
            lang.append(l)
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.writelines(lang)


## process_en_json()
def crowdin_to_mclangcn():
    path1 = r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\zh-CN\processed.json"
    path2 = r"D:\Users\Economy\git\GitHub\mclangcn\texts\zh_CN.lang"
    version_pre = version(read_info(True, r'D:\Users\Economy\git\Gitee\MCBE-lang\object', pre=True))
    print(version_pre)
    path3 = rf"D:\Users\Economy\git\Gitee\MCBE-lang\other\{version_pre}_processed.lang"

    download_translate()

    json_to_lang(path1, path2, path3)

# target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
# process_en_json(f"1.20.0.25_processed.lang", path=target_path, path_append="other",
# json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\processed.json")
# crowdin_to_mclangcn()