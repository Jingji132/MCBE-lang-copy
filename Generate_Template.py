import json
import os
import pickle

import base_fun

default_template = [
    [
        ["vanilla", 0, 0],
        ["oreui", "Ore UI", 0],
        ["persona", 0, 0],
        ["editor", 0, 0],
        ["chemistry", 0, 0],
    ],
    [
        ["custom", 0, "other"]
    ]
]

d_t_json = {
    "text": {
        "vanilla": {
            "display": "",
            "release": None,
            "preview": None
        },
        "oreui": {
            "display": "Ore UI",
            "release": None,
            "preview": None
        },
        "persona": {
            "display": "",
            "release": None,
            "preview": None
        },
        "editor": {
            "display": "",
            "release": None,
            "preview": None
        },
        "chemistry": {
            "display": "",
            "release": None,
            "preview": None
        },
    },
    "other": {
        "custom": {
            "display": "",
            "release": None,
            "preview": None
        }
    }
}


def read(origin_path=r"...\MCBE-lang_UPD_test", append='object'):
    """
    旧版本，即将弃用，迭代：read_json
    """
    if append is not None:
        origin_path = os.path.join(origin_path, append)
    template_file = os.path.join(origin_path, "template")
    try:
        if os.path.isfile(template_file):
            with open(template_file, 'rb+') as f:
                template = pickle.load(f)
                f.close()
        else:
            print("未找到模板文件，将替换为默认模板！")
            template = default_template
    except EOFError:
        print("出错了，将替换为默认模板！")
        template = default_template
    return template


def read_json(path=r"...\MCBE-lang_UPD_test\object\template.json"):
    try:
        if os.path.isfile(path):
            with open(path, 'rb+') as f:
                template = json.load(f)
                f.close()
        else:
            print("未找到模板文件，将替换为默认模板！")
            template = d_t_json
    except EOFError:
        print("出错了，将替换为默认模板！")
        template = d_t_json
    return template


# def save(template, origin_path=r"...\MCBE-lang_UPD_test", append='object',
#          name="template"):
#     """
#     旧版本，即将弃用，迭代：save_json
#     """
#     if append is not None:
#         origin_path = os.path.join(origin_path, append)
#     template_file = os.path.join(origin_path, name)
#     with open(template_file, 'wb') as f:
#         pickle.dump(template, f)
#         f.close()


def save_json(template, path=r"...\MCBE-lang\object\template.json"):
    with open(path, 'w+', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=4)
        f.close()


def old_to_new(old):
    """
    将旧版本模板转换为新版本（json）
    """
    new = {'text': {}}
    for _i in old:
        for _ii in _i:
            name = _ii[0]
            if _ii[2] == 0:
                dir_name = 'text'
            elif isinstance(_ii[2], str):
                dir_name = _ii[2]
                new[dir_name] = {}
            else:
                print(f'旧模板识别出现意外，识别不到文件夹 {_ii[2]} ，转换失败！')
                return None
            if _ii[1] == 0:
                display_name = name.replace('_', ' ').title()
            elif isinstance(_ii[1], str):
                display_name = _ii[1]
            else:
                print(f'旧模板识别出现意外，识别不到显示名称 {_ii[1]} ，转换失败！')
                return None
            new[dir_name][name] = {'display': display_name, 'release': None, 'preview': None}
    return new


# def update(origin_path=r"...\MCBE-lang_UPD_test",
#            path_append_list=None, deny_list=None):
#     """
#         旧版本，即将弃用，迭代：update_json
#     """
#     path = [os.path.join(origin_path, "text")]
#     file_class = [0]
#     if path_append_list is not None:
#         for append in path_append_list:
#             path.append(os.path.join(origin_path, append))
#             file_class.append(append)
#     template = read(origin_path)
#     if deny_list is None:
#         deny_list = ["education", "education_demo", "previewapp", "vanilla_base", "vanilla_vr"]
#     known_list = []
#     for _i in template:
#         for _ii in _i:
#             known_list.append(_ii[0])
#
#     save_template = False
#     for _j in range(len(path)):
#         if not os.path.exists(path[_j]):
#             print("未找到", file_class[_j], "文件夹！")
#             continue
#         folder_list = os.listdir(path[_j])
#         for folder in folder_list:
#             if folder in known_list + deny_list or os.path.isfile(os.path.join(path[_j], folder)):
#                 continue
#             print("发现新文件夹：", folder)
#             save_template = True
#             _modify = input("是否修改显示名称？(Y/n)")
#             while True:
#                 if _modify in ['y', 'Y']:
#                     display = input("请输入：")
#                     break
#                 elif _modify in ['n', 'N']:
#                     display = 0
#                     break
#                 else:
#                     _modify = input("\n输入有误，请重新输入(Y/n)：")
#             template[_j].append([folder, display, file_class[_j]])
#     if save_template:
#         save(template, origin_path)
#     print("模板顺序：")
#     for _i in template:
#         for ii in _i:
#             print(ii[0])
#     return template


def update_json(beta, path=r"...\MCBE-lang_UPD_test", deny_list=None):
    def ensure_display(display_):
        while True:
            ensure_in = input(f"将显示为“{display_.replace('_', ' ').title()}”，确定？（Y/n）")
            if ensure_in in ['Y', 'y']:
                ensure_bool = True
                break
            elif ensure_in in ['N', 'n']:
                ensure_bool = False
                break
            else:
                print("输入有误，重来！")
        return ensure_bool

    template = read_json(rf"{path}\object\template.json")
    if deny_list is None:
        deny_list = ["education", "education_demo", "previewapp", "vanilla_base", "vanilla_vr"]

    beta_str = base_fun.beta_str(beta)

    del_list = []
    for _i in template:
        path_i = os.path.join(path, _i)
        if os.path.exists(path_i):
            dir_list = os.listdir(path_i)
            for dir_ii in dir_list:
                if dir_ii in deny_list:
                    continue
                elif dir_ii in template[_i]:
                    pass
                else:
                    print("发现新文件夹：", dir_ii)
                    while True:
                        display = input("输入显示名称（直接回车使用原名称）：")
                        if display.replace(' ', '') == '':
                            display = ''
                        ensure = ensure_display(dir_ii)
                        if ensure:
                            break
                    template[_i][dir_ii] = {'display': display, 'release': None, 'preview': None}
                template[_i][dir_ii][beta_str] = True

            for _ii in template[_i]:
                path_ii = os.path.join(path_i, _ii)
                if not os.path.exists(path_ii):
                    template[_i][_ii][beta_str] = False
                    print(rf"未找到模板中的文件夹：'{path_i}\{path_ii}'，已标记")
                    if not (template[_i][_ii]['release'] or template[_i][_ii]['preview']):
                        input(rf"将删除'{path_i}\{path_ii}'！")
                        del_list.append([_i, _ii])
        else:
            print(rf"未找到模板中的主文件夹：'{path_i}'，已跳过")
            continue

    for _j in del_list:
        del template[_j[0]][_j[1]]
    save_json(template, rf"{path}\object\template.json")
    print("模板顺序：")
    for _i in template:
        for _ii in template[_i]:
            print(_ii)
    return template


# def modify(path=r"D:\Users\Economy\git\Gitee\MCBE-lang"):
#     """
#     旧版本，即将弃用
#     替代方案：手动修改json文件,或自动识别并删除旧的包信息
#     """
#     global i, j
#
#     def mod_find():
#         i_num = 0
#         for i_val in template:
#             j_num = 0
#             for j_val in i_val:
#                 if name == j_val[0]:
#                     return i_num, j_num
#                 j_num += 1
#             i_num += 1
#         print("未找到内容！")
#         return None, None
#
#     def mod_display(_i, _j):
#         display = input("显示名称 [返回(Enter)]：")
#         if display == '':
#             return False
#         elif display == '0':
#             display = 0
#         template[_i][_j][1] = display
#         print("当前模板：\n", template)
#         return True
#
#     def mod_locate(_i, _j):
#         j_o = _j
#         while True:
#             move = input("[前移(A)] [后移(D)] [返回(Enter)]：")
#             if move in ['a', 'A'] and _j != 0:
#                 t = template[_i][_j - 1]
#                 template[_i][_j - 1] = template[_i][_j]
#                 template[_i][_j] = t
#                 _j -= 1
#                 print("当前模板：\n", template)
#             elif move in ['d', 'D'] and _j != len(template[_i]):
#                 t = template[_i][_j + 1]
#                 template[_i][_j + 1] = template[_i][_j]
#                 template[_i][_j] = t
#                 _j += 1
#                 print("当前模板：\n", template)
#             elif move == '':
#                 if j_o == _j:
#                     return False
#                 else:
#                     return True
#             else:
#                 continue
#
#     def mod_delete(_i, _j):
#         info = "确认要删除" + template[_i][_j][0] + "吗？[确认(Yes)] [取消(任意)]"
#         confirm = input(info)
#         if confirm in ['Yes', 'yes']:
#             del template[_i][_j]
#             print("当前模板：\n", template)
#             return True
#         else:
#             print("已取消删除")
#             return False
#
#     template = read(path)
#     print("当前模板：\n", template)
#     old_finished = True
#     while True:
#         break_flag = False
#         while True:
#             if not old_finished:
#                 break
#             name = input("修改内容 [退出(Enter)]：")  # 例如：experimental_cameras，若直接回车则退出
#             if name == '':
#                 print("退出")
#                 break_flag = True
#                 break
#             i, j = mod_find()
#             if i is not None:
#                 break
#         if break_flag:
#             break
#         while True:
#             mod_num = 0
#             mod = input("[取消(Enter)] [修改名称(1)] [移动位置(2)] [删除(3)]：")
#             if mod == '':
#                 old_finished = True
#                 break
#             elif int(mod) in range(4):
#                 mod_num = int(mod)
#                 break
#             else:
#                 print("请输入正确的数字！")
#         if mod == '' or mod_num == 0:
#             continue
#         elif mod_num == 1:
#             old_finished = mod_display(i, j)
#         elif mod_num == 2:
#             old_finished = mod_locate(i, j)
#         elif mod_num == 3:
#             old_finished = mod_delete(i, j)
#     old_template = read(path)
#     if template == old_template:
#         print("未更改")
#         return
#     else:
#         save_temp = input("保存更改？[确认(Y)][取消(任意)]")
#         if save_temp in ['y', 'Y']:
#             save(template, path)
#             print("已保存\n当前模板：\n", template)
#         else:
#             print("未更改")
#             return


# update(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
#        path_append_list=["other"])
# modify()

if __name__ == '__main__':
    # old_template = read(r"D:\Users\Economy\git\Gitee\MCBE-lang")
    # print(old_template)
    # new_template = old_to_new(old_template)
    # print(new_template)
    # save_json(new_template, r"D:\Users\Economy\git\Gitee\MCBE-lang\object\template.json")
    update_json(True, r"D:\Users\Economy\git\Gitee\MCBE-lang")
