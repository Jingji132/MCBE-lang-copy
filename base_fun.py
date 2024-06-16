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
