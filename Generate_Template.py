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


def update(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
           path_append_list=None, deny_list=None):
    path = [os.path.join(origin_path, "text")]
    file_class = [0]
    if path_append_list is not None:
        for append in path_append_list:
            path.append(os.path.join(origin_path, append))
            file_class.append(append)
    template_file = os.path.join(origin_path, "template")
    try:
        if os.path.isfile(template_file):
            with open(template_file, 'rb+') as f:
                template = pickle.load(f)
                f.close()
        else:
            template = default_template
    except EOFError:
        template = default_template

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
        with open(template_file, 'wb') as f:
            pickle.dump(template, f)
            f.close()
    # print(template)
    template_final = []
    print("模板顺序：")
    for i in template:
        for ii in i:
            template_final.append(ii)
            print(ii[0])
    # print(template_final)
    return template_final


def modify(path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test"):
    template_file = os.path.join(path, "template")

    def temp_find():
        try:
            if os.path.isfile(template_file):
                with open(template_file, 'rb+') as f:
                    temp = pickle.load(f)
                    f.close()
            else:
                print("未找到模板文件，将替换为默认模板！")
                temp = default_template
        except EOFError:
            print("出错了！")
            return
        print("当前模板：\n", temp)
        return temp

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
        display = input("显示名称更改为：")
        if display == '0':
            display = 0
        template[i][j][1] = display
        print("当前模板：\n", template)

    def mod_locate(i, j):
        while True:
            move = input("[前移(A)] [后移(D)] [返回(B)]：")
            if move in ['a', 'A'] and j != 0:
                t = template[i][j - 1]
                template[i][j - 1] = template[i][j]
                template[i][j] = t
                print("当前模板：\n", template)
            elif move in ['d', 'D'] and j != len(template[i]):
                t = template[i][j + 1]
                template[i][j + 1] = template[i][j]
                template[i][j] = t
                print("当前模板：\n", template)
            elif move in ['b', 'B']:
                return
            else:
                continue

    def mod_delete(i, j):
        del template[i][j]
        print("当前模板：\n", template)

    template = temp_find()

    while True:
        while True:
            name = input("修改内容 [退出(0)]：")  # experimental_cameras
            if name == '0':
                print("退出")
                return
            i, j = mod_find()
            if i is not None:
                break
        while True:
            mod_num = int(input("[取消(0)] [修改名称(1)] [移动位置(2)] [删除(3)]："))
            if mod_num in range(4):
                break
            else:
                print("请输入正确的数字！")
        if mod_num == 0:
            print("未进行更改！")
        elif mod_num == 1:
            mod_display(i, j)
        elif mod_num == 2:
            mod_locate(i, j)
        elif mod_num == 3:
            mod_delete(i, j)
        cont = input("继续更改？[确认(Y)][取消(任意)]")
        if cont in ['y', 'Y']:
            continue
        else:
            break

    print("当前模板：\n", template)
    with open(template_file, 'wb') as f:
        pickle.dump(template, f)
        f.close()


temp = [
    ["vanilla", 0, 0],
    ["oreui", "Ore UI", 0],
    ["persona", 0, 0],
    ["editor", 0, 0],
    ["experimental_cameras", 0, 0],
    ["chemistry", 0, 0],
    ["custom", 0, "other"]
]

# update(origin_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
#        path_append_list=["other"])
modify()
