# 更新Crowdin
import csv
import json
import os.path
import pickle

import Convert_Lang
import Produce_Lang
import Update_Lang
import crowdin


def pre_release(ver):
    """
    :param ver: '[x, x, x, x]' 想要将Pre-release回退到的版本，如'1.21.0.26'为[1, 21, 0, 26]
    :return:
    """
    version = Update_Lang.version(ver)
    target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    json_path = r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\processed.json"

    Convert_Lang.process_en_json(f"{version}_processed.lang", path=target_path, path_append="other",
                                 json_path=json_path)
    crowdin.update_branch("Pre-Release", version, reset=False)
    with open(r"D:\Users\Economy\git\Gitee\MCBE-lang\object\Pre-release", 'wb') as f:
        pickle.dump(ver, f)
        f.close()


def change_version(ver, ver_type='Preview'):
    """
    :param ver_type: 'Preview' 'Release' 'Pre-Release'
    :param ver: [xx, xx, xx, xx]
    :return:
    """
    version = Update_Lang.version(ver)
    target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    json_path = fr"D:\Users\Economy\git\Gitee\lang-crowdin\{ver_type}\processed.json"

    Convert_Lang.process_en_json(f"{version}_processed.lang", path=target_path, path_append="other",
                                 json_path=json_path)
    crowdin.update_branch(ver_type, version, reset=False)
    with open(rf"D:\Users\Economy\git\Gitee\MCBE-lang\object\{ver_type}", 'wb') as f:
        pickle.dump(ver, f)
        f.close()


def change_version_obj(ver_name, path=r"D:\Users\Economy\git\Gitee\MCBE-lang\object"):
    path = os.path.join(path, ver_name)
    with open(path, 'rb+') as f:
        print(pickle.load(f))
        f.close()
    y_o_n = input("修改？(Y)")
    if y_o_n == 'Y':
        ver = [0, 0, 0, 0]
        for i in range(4):
            ver[i] = int(input(f"第{i}位版本："))
        with open(path, 'wb') as f:
            pickle.dump(ver, f)
            f.close()


def show_object(path=r"D:\Users\Economy\git\Gitee\MCBE-lang\object"):
    p_list = os.listdir(path)
    print('list:\t', p_list, '\n')
    for filename in p_list:
        filepath = os.path.join(path, filename)
        with open(filepath, 'rb+') as f:
            obj = pickle.load(f)
            print(filename, ':\t', obj, '\ttype:', type(obj))
            f.close()


def lang_init(path=r"D:\Users\Economy\git\Gitee\MCBE-lang-test1"):
    # n_path = rf'{path}\object'
    # os.makedirs(n_path)
    for beta in [True, False]:
        for pre in [True, False]:
            # print(beta, pre)
            Update_Lang.update_info(beta, path, 'object', pre=pre)

    return


target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"


def info_o2n():
    P = Update_Lang.read_info(True, target_path, 'object')
    R = Update_Lang.read_info(False, target_path, 'object')
    PR = Update_Lang.read_info(True, target_path, 'object', pre=True)

    new = {'Preview': P, 'Release': R, 'Pre-release': PR}
    print(new)

    with open(rf'{target_path}/object/Version_info.json', 'w+', encoding='utf-8') as f:
        json.dump(new, f, indent=4)


def get_translation_csv(path):
    Produce_Lang.process(path, r'temp\trans_pro.lang')
    trans_dict = Convert_Lang.processed_to_dict(r'temp\trans_pro.lang')
    # print(trans_dict)
    headers = ['Key', 'Source string', 'Context', 'Translation']
    rows = []
    for key in trans_dict:
        if '.' in key:
            s_key = '"' + key + '"'
        else:
            s_key = key
        rows.append((s_key, None, None, trans_dict[key]))
    with open(r'temp\trans_out.csv', 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


if __name__ == '__main__':
    info_o2n()

    # get_translation_csv(r"D:\Users\Economy\Downloads\zh_TW.lang")

    # lang_init()
    # show_object(r"D:\Users\Economy\git\Gitee\MCBE-lang\object")
    #
    # Update_Lang.update_info(beta=True, path=r'D:\Users\Economy\git\Gitee\MCBE-lang\object',
    #                         crowdin=False)
    #
    # show_object(r"D:\Users\Economy\git\Gitee\MCBE-lang\object")

    # csv_path = r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.csv"
    # with open(csv_path, 'r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     new_rows = []
    #     for row in reader:
    #         if row[int('Key')] in ["tips.game.3"]:
    #             print(row[int('Key')])
