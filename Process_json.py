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
    for line in lines:
        if "++ b/text" in line:
            continue
        else:
            line = line.split('\t')
            if "##" in line[0] or line[0] in ['', ' ', '\n', ' \n']:
                continue
            elif simple:
                if '#' in line[1]:
                    print("文件有问题，正文出现注释！")
                    line[1] = line[1].split('#')[0]
                add_dict[line[0]] = line[1].replace('\n', '')
            else:
                if '#' not in line[2]:
                    print(line, "：未以#结尾，已自动添加")
                    line[2] = '#' + line[2]
                add_dict[line[0]] = [line[1], line[2]]
    return add_dict


def processed_to_dict_new(lang_path):
    add_dict = {}
    with open(lang_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split('\t')
        if "##" in line[0] or line[0] in ['', ' ', '\n', ' \n']:
            continue
        elif len(line) > 2:
            add_dict[line[0]] = {"text": line[1], "crowdinContext": line[2]}
            print(line)
        else:
            add_dict[line[0]] = {"text": line[1], "crowdinContext": ''}
    return add_dict


def process_zh_json():
    path2 = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    path3 = r"D:\Users\Economy\git\Gitee\lang-crowdin\en"
    path4 = os.path.join(path3, 'processed.lang')
    path1 = os.path.join(path3, 'processed.json')

    lang_to_process('zh_CN.lang', origin_path=path2, path=path3)
    with open(path1, 'w+', encoding='utf-8') as f:
        json.dump(processed_to_dict(path4, True), f, ensure_ascii=False)


def process_en_json(process, path=r"D:\Users\Economy\git\Gitee\MCBE-lang", path_append=None,
                    json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin1\Preview\processed.json"):
    if path_append is not None:
        path = os.path.join(path, path_append, process)
    else:
        path = os.path.join(path, process)

    with open(json_path, 'w+', encoding='utf-8') as f:
        json.dump(processed_to_dict_new(path), f, ensure_ascii=False)


def json_to_lang(json_path, lang_path, template):
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = json.load(f)
    with open(template, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lang = []
    for l in lines:
        l_list = l.split('\t')
        if '#' in l_list[0]:
            lang.append(l)
            continue
        elif l_list[0] in lang_dict:
            l_list[1] = lang_dict[l_list[0]]
            if len(l_list) == 2:
                lzh = l_list[0] + '=' + l_list[1] + '\t#\n'
            elif len(l_list) == 3:
                lzh = l_list[0] + '=' + l_list[1] + '\t#' + l_list[2]
            else:
                print("出错：" + l_list[0])
                lzh = l
            lang.append(lzh)
        else:
            lang.append(l)
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.writelines(lang)


## process_en_json()
def crowdin_to_mclangcn(pre=True):
    if pre:
        ver = 'Pre-'
    else:
        ver = ''
    path1 = fr"D:\Users\Economy\git\Gitee\lang-crowdin\{ver}Release\zh-CN\processed.json"
    path2 = r"D:\Users\Economy\git\GitHub\mclangcn\texts\zh_CN.lang"
    version_pre = version(read_info(True, r'D:\Users\Economy\git\Gitee\MCBE-lang\object', pre=True)['ver'])
    print(version_pre)
    path3 = rf"D:\Users\Economy\git\Gitee\MCBE-lang\other\{version_pre}_processed.lang"

    download_translate()

    json_to_lang(path1, path2, path3)


# target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
# process_en_json(f"1.20.0.25_processed.lang", path=target_path, path_append="other",
# json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\processed.json")
# crowdin_to_mclangcn()

# process_zh_json()

# path_lang = r"D:\test"  # ←←←要读取的lang文件所在路径（不含文件名称）
# path_save = r"D:\test"  # ←←←要保存的json文件所在路径（不含文件名称）
# lang_to_process('en_US.lang', "processed.lang", path=path_save, origin_path=path_lang)
# # ↑↑↑首个参数是要读取的lang文件名称，当前为”en_US.lang“↑↑↑
# process_en_json("processed.lang", path=path_save, json_path=os.path.join(path_save, 'processed.json'))
# # ↑↑↑末尾位置的”processed.json“是要保存的json文件名称↑↑↑
# #

if __name__ == '__main__':
    # processed_to_dict_new(r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.10.23_processed.lang")
    process_en_json(f"1.21.10.23_processed.lang", path_append="other")
