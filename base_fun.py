import os.path


def make_dir(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        return


def make_dir_path(path):
    dir_path = os.path.dirname(path)
    if os.path.exists(dir_path):
        return
    else:
        os.makedirs(dir_path)
        return


def replace_rule(input_line):
    temp_line = input_line.replace("\t", "")  # 去除多余制表符
    output_line = temp_line.replace("#", "\t#", 1).replace("=", "\t", 1)  # 保留必要制表符
    return output_line


def beta_str(beta, up=False):
    if beta:
        b_str = 'preview'
    else:
        b_str = 'release'
    if up:
        b_str = b_str.title()
    return b_str


def compare_ver(ver1, ver2, complex_return=False):
    flag1 = False  # 判断ver1是否大于ver2
    i = 0
    for i in ver1:
        if ver1[i] == ver2[i]:
            i += 1
            continue
        elif ver1[i] > ver2[i]:
            flag1 = True
            break
        elif ver1[i] < ver2[i]:
            flag1 = False
            break
        else:
            print("版本比较时出错！")
            continue
    if complex_return:
        if i < 3:
            flag2 = True
        else:
            flag2 = False
        return flag1, flag2
    else:
        return flag1
