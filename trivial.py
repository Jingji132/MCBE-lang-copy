import os
from random import randint
import requests
import difflib

import Convert_Lang
import Generate_Template
import Produce_Lang
import crowdin


def find_in_dict(the_dict, key, full=True):
    if key in the_dict:
        if full:
            return the_dict[key]
        else:
            return the_dict[key][0]
    else:
        return ''


def fuzzy_matching(texts_list, value, similarity=0.8, max=1):
    texts_score = {}
    for i in texts_list:
        score = difflib.SequenceMatcher(None, i, value).quick_ratio()
        if score < similarity:
            continue
        texts_score[i] = score
        if score > max:
            break
    texts_score = sorted(texts_score.items(), key=lambda x: x[1], reverse=False)
    if len(texts_score) > 0:
        match_value = texts_score[-1][0]
        return match_value, texts_score[-1][1]
    else:
        return '', 0


def update_custom_tips(path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
                       read_path=r"text\vanilla\en_US.lang",
                       mod_path=r"other\custom\en_US.lang"):
    read_path = os.path.join(path, read_path)
    mod_path = os.path.join(path, mod_path)
    if not (os.path.isfile(read_path) and os.path.isfile(mod_path)):
        print("路径错误！")
        return
    tips = "tips.game."
    with open(mod_path, 'r', encoding='utf-8') as f:
        origin_lines = f.readlines()
        f.close()
    with open(read_path, 'r', encoding='utf-8') as f:
        read_lines = f.readlines()
        f.close()
    num1 = 0
    for line in origin_lines:
        if tips in line:
            num1 = int(line.split("=")[0].replace(tips, ""))
            # print(num1)
            break
    if num1 == 0:
        print("文件不包含tips！")
        return
    num2 = 0
    for line in read_lines:
        if tips in line:
            num2 += 1
    # print(num2)
    if num2 == num1 - 1:
        print("tips序号无需更新\n")
        return
    print("tips序号待更新")
    num = num2 + 1
    mod_lines = []
    # print(tips_num)
    for line in origin_lines:
        tips_num = tips + str(num)
        tips_num1 = tips + str(num1)
        line = line.replace(tips_num1, tips_num)
        # print(line)
        mod_lines.append(line)
        num += 1
        num1 += 1

    with open(mod_path, 'w', encoding='utf-8') as f:
        f.writelines(mod_lines)
        print("更新完成\n")
        f.close()


def get_url(url, time_set=200):
    headers = {
        'user-agent': f'Mozilla/5.0 (Linux; Android {randint(6, 14)}; OnePlus {randint(7, 11)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'}
    response = None
    for time in range(time_set, time_set + 3):
        try:
            response = requests.get(url, headers=headers, timeout=time)
            break
        except:
            time += 1
            continue
    if response is None:
        print("请求超时！")
        return None
    else:
        return response


def only_zh_upd(diff_list):
    for i in diff_list:
        for j in i:
            if 'en_US.lang' in j:
                return False
    return True


# get_url('https://google.com', 5)
def test_for_copy2():
    paths = os.walk(
        r"C:\Program Files\WindowsApps\Microsoft.MinecraftWindowsBeta_1.20.5022.0_x64__8wekyb3d8bbwe\data\resource_packs")
    print('\n')
    path_list = []
    for path, dir_lst, file_lst in paths:
        for dir_name in dir_lst:
            if dir_name == 'texts':
                path_list.append(os.path.join(path, dir_name))
    for path in path_list:
        short_path = path.split(r"x64__8wekyb3d8bbwe\data\resource_packs")[1]
        stp = short_path.replace("\\", '', 1).replace(r'\texts', '', 1)
        stp_ = stp.replace('\\', '_')
        print(stp_)


def add_bad_translation(template=None,
                        target_path=r"D:\Users\Economy\git\Gitee\MCBE-lang",
                        zh_merged_path=r"D:\Users\Economy\git\Gitee\MCBE-lang\test\zh_BAD.lang",
                        csv_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.csv"):
    Produce_Lang.save(template, target_path, zh_merged_path, zh=True)
    zh_dict = Convert_Lang.lang_to_dict(zh_merged_path)
    Convert_Lang.csv_add_context(zh_dict, csv_path, '基翻：')


if __name__ == '__main__':
    # target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    # template = Generate_Template.read(target_path)
    # add_bad_translation(template, target_path,
    #                     r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.0.26_zh_BAD.lang",
    #                     r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\processed.csv")

    # crowdin.update_branch('Pre-Release')

    if False:
        print(1)
