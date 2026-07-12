import os.path, random


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
    for i in range(4):
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


def ver_type_str(beta, pre=False):
    if beta:
        if pre:
            return 'Pre-release'
        else:
            return 'Preview'
    else:
        return 'Release'


def ver_str(ver, full=True):
    if full:
        version = str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "." + str(ver[3])
    else:
        version = str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2])
    return version

def ver_str_dis(ver, full=True):
    if full:
        version = str(ver[1]) + "." + str(ver[2]) + "." + str(ver[3])
    else:
        version = str(ver[1]) + "." + str(ver[2])
    return version

def sample_dict(d, ratio:float=0.001):
    if not d:
        return {}
    k = max(1, int(len(d) * ratio))
    selected_keys = random.sample(list(d.keys()), min(k, len(d)))
    return {key: d[key] for key in selected_keys}
def sample_and_ver(d:dict, version:str='0.0.0'):
    d1=sample_dict(d)
    d1['version.name']={'text':version, 'crowdinContext':'string for debug'}
    return d1


if __name__ == '__main__':
    dd = {i: f"value_{i}" for i in range(5000)}
    dd2 = sample_dict(dd)
    print(len(dd),"\n",len(dd2))
    # print(sample_dict(dd))
    pass
