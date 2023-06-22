import os
import pickle

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


def read(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", append='object'):
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


def save(template, origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", append='object'):
    if append is not None:
        origin_path = os.path.join(origin_path, append)
    template_file = os.path.join(origin_path, "template")
    with open(template_file, 'wb') as f:
        pickle.dump(template, f)
        f.close()


def update(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
           path_append_list=None, deny_list=None):
    path = [os.path.join(origin_path, "text")]
    file_class = [0]
    if path_append_list is not None:
        for append in path_append_list:
            path.append(os.path.join(origin_path, append))
            file_class.append(append)
    template = read(origin_path)
    if deny_list is None:
        deny_list = ["education", "education_demo", "previewapp", "vanilla_base", "vanilla_vr"]
    known_list = []
    for i in template:
        for ii in i:
            known_list.append(ii[0])

    save_template = False
    for j in range(len(path)):
        if not os.path.exists(path[j]):
            print("未找到", file_class[j], "文件夹！")
            continue
        folder_list = os.listdir(path[j])
        for folder in folder_list:
            if folder in known_list + deny_list or os.path.isfile(os.path.join(path[j], folder)):
                continue
            print("发现新文件夹：", folder)
            save_template = True
            modify = input("是否修改显示名称？(Y/n)")
            while True:
                if modify in ['y', 'Y']:
                    display = input("请输入：")
                    break
                elif modify in ['n', 'N']:
                    display = 0
                    break
                else:
                    modify = input("\n输入有误，请重新输入(Y/n)：")
            template[j].append([folder, display, file_class[j]])
    if save_template:
        save(template, origin_path)
    print("模板顺序：")
    for i in template:
        for ii in i:
            print(ii[0])
    return template


def modify(path=r"D:\Users\Economy\git\Gitee\MCBE-lang"):
    global i, j

    def mod_find():
        i_num = 0
        for i_val in template:
            j_num = 0
            for j_val in i_val:
                if name == j_val[0]:
                    return i_num, j_num
                j_num += 1
            i_num += 1
        print("未找到内容！")
        return None, None

    def mod_display(i, j):
        display = input("显示名称 [返回(Enter)]：")
        if display == '':
            return False
        elif display == '0':
            display = 0
        template[i][j][1] = display
        print("当前模板：\n", template)
        return True

    def mod_locate(i, j):
        j_o = j
        while True:
            move = input("[前移(A)] [后移(D)] [返回(Enter)]：")
            if move in ['a', 'A'] and j != 0:
                t = template[i][j - 1]
                template[i][j - 1] = template[i][j]
                template[i][j] = t
                j -= 1
                print("当前模板：\n", template)
            elif move in ['d', 'D'] and j != len(template[i]):
                t = template[i][j + 1]
                template[i][j + 1] = template[i][j]
                template[i][j] = t
                j += 1
                print("当前模板：\n", template)
            elif move == '':
                if j_o == j:
                    return False
                else:
                    return True
            else:
                continue

    def mod_delete(i, j):
        info = "确认要删除" + template[i][j][0] + "吗？[确认(Yes)] [取消(任意)]"
        confirm = input(info)
        if confirm in ['Yes', 'yes']:
            del template[i][j]
            print("当前模板：\n", template)
            return True
        else:
            print("已取消删除")
            return False

    template = read(path)
    print("当前模板：\n", template)
    old_finished = True
    while True:
        break_flag = False
        while True:
            if not old_finished:
                break
            name = input("修改内容 [退出(Enter)]：")  # 例如：experimental_cameras，若直接回车则退出
            if name == '':
                print("退出")
                break_flag = True
                break
            i, j = mod_find()
            if i is not None:
                break
        if break_flag:
            break
        while True:
            mod_num = 0
            mod = input("[取消(Enter)] [修改名称(1)] [移动位置(2)] [删除(3)]：")
            if mod == '':
                old_finished = True
                break
            elif int(mod) in range(4):
                mod_num = int(mod)
                break
            else:
                print("请输入正确的数字！")
        if mod == '' or mod_num == 0:
            continue
        elif mod_num == 1:
            old_finished = mod_display(i, j)
        elif mod_num == 2:
            old_finished = mod_locate(i, j)
        elif mod_num == 3:
            old_finished = mod_delete(i, j)
    old_template = read(path)
    if template == old_template:
        print("未更改")
        return
    else:
        save_temp = input("保存更改？[确认(Y)][取消(任意)]")
        if save_temp in ['y', 'Y']:
            save(template, path)
            print("已保存\n当前模板：\n", template)
        else:
            print("未更改")
            return




# update(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
#        path_append_list=["other"])
# modify()
