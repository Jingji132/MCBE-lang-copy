from Update_Lang import read_info
from mclangcn_process import lang_to_process, processed_to_dict
from trivial import only_zh_upd
from git_fun import diff
from trivial import find_in_dict
from JE_lang import find_je_lang
import os


def old_process():
    path = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    lang_to_process(origin_path=path,
                    origin='zh_CN.lang',
                    processed="processed.lang",
                    path=r"D:\Users\Economy\git\Github\mclangcn-update")


def diff_process():
    path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    lang_to_process(origin_path=path,
                    origin='diff1.lang',
                    processed="diff.lang",
                    path=path)


def read_diff(path=r"D:\Users\Economy\git\Gitee\MCBE-lang", name='diff.lang'):
    def stop_and_reset(l, deny):
        if "diff --git a/text" in l:
            stop = True
            for d in deny:
                if d in l:
                    reset = False
                    return stop, reset
            reset = True
        else:
            stop, reset = False, False
        return stop, reset

    read_path = os.path.join(path, name)
    ready_to_read = False
    ready_to_en = False
    ready_to_zh = False
    with open(read_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    en = []
    zh = []
    for l in lines:
        stop, reset = stop_and_reset(l, ['/previewapp/', '/education/', '/education_demo/', '/vanilla_vr/'])
        if stop:
            ready_to_en = False
            ready_to_zh = False
        if reset:
            ready_to_read = True

        if ready_to_read and '+++' in l:
            if 'en_US.lang' in l:
                ready_to_en = True
            elif 'zh_CN.lang' in l:
                ready_to_zh = True

        if ready_to_en:
            en.append(l)
        elif ready_to_zh:
            zh.append(l)

    return en, zh


def process_diff(lang_list):
    lang_dict = {}
    comment_dict = {}
    for i in lang_list:
        list = i.split('\t')
        if list[0][0] in ['-', ' ', '@']:
            continue
        length = len(list)
        if length > 3:
            print("出现len为", len(list), "的列表：\n", list)
            print("请检查！")
            return
        elif length == 3:
            if '#' in list[1]:
                print("出现有注释但注释在正文位置的列表：\n", list)
                print("请检查！")
                return
            else:
                lang_dict[list[0][1:]] = [list[1], list[2]]
                comment_dict[list[0][1:]] = [list[1], list[2]]
        elif length == 2:
            if '#' in list[1]:
                print("出现有注释但注释在正文位置的列表：\n", list)
                print("请检查！")
                return
            else:
                lang_dict[list[0][1:]] = [list[1][:-1], '\n']
    return lang_dict, comment_dict


def create_translate(lang_dict, be_dict, old_dict, old_en_dict, je_en_dict, je_zh_dict):
    je_en_redict = dict(zip(je_en_dict.values(), je_en_dict.keys()))
    old_en_redict = dict(zip(old_en_dict.values(), old_en_dict.keys()))
    trans_list = []
    for key in lang_dict:
        original = lang_dict[key][0]
        comment = lang_dict[key][1][:-1]

        be_translate = find_in_dict(be_dict, key, False)

        st_key = find_in_dict(je_en_redict, original)
        st_translate = find_in_dict(je_zh_dict, st_key)

        bf_translate = find_in_dict(old_dict, key)

        fd_key = find_in_dict(old_en_redict, original)
        if fd_key != '':
            fd_translate = find_in_dict(old_dict, fd_key)
        else:
            fd_translate = ''
            pass

        t_list = [key, original, comment, be_translate, st_translate, bf_translate, fd_translate]
        trans_list.append(t_list)
    print(trans_list[0])
    return trans_list
    # for list in trans_list:
    # print(list)


def fun1():
    # diff_process()
    old_process()
    path = r"D:\Users\Economy\git\Github\mclangcn-update"
    old_path = os.path.join(path, "processed.lang")

    path_ver = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    ver = read_info(False, path_ver, 'object')
    version = str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + " release"
    name = version + '_processed.lang'
    path1 = r"D:\Users\Economy\git\Gitee\MCBE-lang\other"
    old_en = processed_to_dict(os.path.join(path1, name), True)

    old = processed_to_dict(old_path, True)
    en, zh = read_diff()
    la, co = process_diff(en)
    be_zh, co_zh = process_diff(zh)
    je_en, je_zh = find_je_lang()
    tr_list = create_translate(la, be_zh, old, old_en, je_en, je_zh)
    save_path = os.path.join(path, 'save.lang')
    with open(save_path, 'w', encoding='utf-8') as f:
        for t_list in tr_list:
            for t in t_list:
                f.writelines(t + '\t')
            f.writelines('\n')


def fun2():
    dl = diff()
    if only_zh_upd(dl):
        print("此版本是预发布版！")
    else:
        print("此版本不是预发布版！")

fun2()
