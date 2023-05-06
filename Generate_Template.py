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
    print(template)
    template_final = []
    for i in template:
        for ii in i:
            template_final.append(ii)
    print(template_final)


def modify(path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test"):
    template_file = os.path.join(path, "template")
    try:
        if os.path.isfile(template_file):
            with open(template_file, 'rb+') as f:
                template = pickle.load(f)
                f.close()
        else:
            print("未找到模板文件，将替换为默认模板！")
            template = default_template
    except EOFError:
        print("出错了！")
        return
    print("当前模板：\n", template)
    name = input("修改内容：")   # experimental_cameras
    i_num, ii_num = 0, 0
    break_flag = False
    for i in template:
        for ii in i:
            if name == ii[0]:
                display = input("\n显示名称更改为：")
                break_flag = True
                if display == '0':
                    display = 0
                template[i_num][ii_num][1] = display
                break
            ii_num += 1
        if break_flag:
            break
        i_num += 1
    if not break_flag:
        print("未进行更改！")
        return
    print("修改后模板：\n", template)
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
#       path_append_list=["other"])
modify()