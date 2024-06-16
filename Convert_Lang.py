import csv
import json
import os

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


def processed_to_dict(lang_path):
    add_dict = {}
    with open(lang_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split('\t')
        if "##" in line[0] or line[0] in ['', ' ', '\n', ' \n']:
            continue
        elif '#' in line[1]:
            print("文件有问题，正文出现注释！")
            line[1] = line[1].split('#')[0]
        add_dict[line[0]] = line[1].replace('\n', '')
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
            add_dict[line[0]] = {"text": line[1].replace('\n', ''), "crowdinContext": line[2]}
            # print(line)
        else:
            add_dict[line[0]] = {"text": line[1].replace('\n', ''), "crowdinContext": ''}
    return add_dict


def convert_zh_lang(is_json=False, is_csv=False):
    source_path = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    process_path = r"D:\Users\Economy\git\Gitee\lang-crowdin\mclangcn"
    lang_to_process('zh_CN.lang', origin_path=source_path, path=process_path)

    path4 = os.path.join(process_path, 'processed.lang')

    if is_json:
        convert_path = os.path.join(process_path, 'processed.json')
        with open(convert_path, 'w+', encoding='utf-8') as f:
            json.dump(processed_to_dict(path4), f, ensure_ascii=False)

    if is_csv:
        input_path = r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.0 release_processed.lang"
        the_dict = processed_to_dict_new(input_path)
        lang_dict = processed_to_dict(path4)
        convert_path = os.path.join(process_path, 'processed.csv')
        headers = ['Key', 'Source string', 'Context', 'Translation']
        rows = []
        for key in the_dict:
            rows.append((key, the_dict[key]['text'], the_dict[key]['crowdinContext'], lang_dict[key]))
        with open(convert_path, 'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)


def process_en_json(process, path=r"D:\Users\Economy\git\Gitee\MCBE-lang", path_append=None,
                    json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin1\Preview\processed.json"):
    if path_append is not None:
        path = os.path.join(path, path_append, process)
    else:
        path = os.path.join(path, process)

    with open(json_path, 'w+', encoding='utf-8') as f:
        json.dump(processed_to_dict_new(path), f, ensure_ascii=False)


def process_csv(input_path=r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.0 release_processed.lang",
                output_path=r"D:\Users\Economy\git\Gitee\lang-crowdin1\Preview\processed.csv",
                special_key=True):
    headers = ['Key', 'Source string', 'Context', 'Translation']
    the_dict = processed_to_dict_new(input_path)
    rows = []
    if special_key:
        for key in the_dict:
            if '.' in key:
                s_key = '"'+key+'"'
            else:
                s_key = key
            rows.append((s_key, the_dict[key]['text'], the_dict[key]['crowdinContext']))
    else:
        for key in the_dict:
            rows.append((key, the_dict[key]['text'], the_dict[key]['crowdinContext']))
    with open(output_path, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def json_to_lang(json_path, lang_path, template):
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = json.load(f)
    with open(template, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lang = []
    for line in lines:
        l_list = line.split('\t')
        if '#' in l_list[0]:
            lang.append(line)
            continue
        elif l_list[0] in lang_dict:
            l_list[1] = lang_dict[l_list[0]]
            if len(l_list) == 2:
                lzh = l_list[0] + '=' + l_list[1] + '\t#\n'
            elif len(l_list) == 3:
                lzh = l_list[0] + '=' + l_list[1] + '\t#' + l_list[2]
            else:
                print("出错：" + l_list[0])
                lzh = line
            lang.append(lzh)
        else:
            lang.append(line)
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.writelines(lang)


# process_en_json()
def crowdin_to_mclangcn_json(pre=True):
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


def csv_to_lang(csv_path, lang_path, temp_path):
    lang_dict = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[0].replace('"', '')
            lang_dict[key] = row[3]
            # print(row[0])
    with open(temp_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lang = []
    for line in lines:
        l_list = line.split('\t')
        if '#' in l_list[0]:
            lang.append(line)
            continue
        elif l_list[0] in lang_dict:
            l_list[1] = lang_dict[l_list[0]]
            # print(l_list[1])
            if len(l_list) == 2:
                lzh = l_list[0] + '=' + l_list[1] + '\t#\n'
            elif len(l_list) == 3:
                lzh = l_list[0] + '=' + l_list[1] + '\t#' + l_list[2]
            else:
                print("出错：" + l_list[0])
                lzh = line
            # print(lzh)
            lang.append(lzh)
        else:
            lang.append(line)
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.writelines(lang)


def crowdin_to_mclangcn_csv(pre=True):
    if pre:
        ver = 'Pre-'
    else:
        ver = ''
    path1 = fr"D:\Users\Economy\git\Gitee\lang-crowdin\{ver}Release\zh-CN\processed.csv"
    path2 = r"D:\Users\Economy\git\GitHub\mclangcn\texts\zh_CN.lang"
    version_v = version(read_info(beta=pre, path=r'D:\Users\Economy\git\Gitee\MCBE-lang\object', pre=pre)['ver'])
    print(version_v)
    if not pre:
        version_l = version_v.split('.')
        version_v = version_l[0]+'.'+version_l[1]+'.'+version_l[2]+' Release'
    path3 = rf"D:\Users\Economy\git\Gitee\MCBE-lang\other\{version_v}_processed.lang"

    download_translate(pre)

    csv_to_lang(path1, path2, path3)


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
    # process_en_json(f"1.21.0 release_processed.lang", path=r"D:\Users\Economy\git\Gitee\MCBE-lang",
    #                 path_append="other",
    #                 json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\Release\processed.json")
    # process_zh_json()

    # crowdin_to_mclangcn_csv(False)
    # crowdin_to_mclangcn_csv(False)
    # convert_zh_lang(True, True)

    v_name = ['Preview', 'Pre-Release', 'Release']
    v_n = v_name[0]  # 0 1 2
    process_csv(r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.10.23_processed.lang",
                rf"D:\Users\Economy\git\Gitee\lang-crowdin\{v_n}\processed.csv")
