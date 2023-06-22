import os
import shutil
import pickle


def find(beta=True):
    folder_path_pre = r"C:\Program Files\WindowsApps"
    find_list = os.listdir(folder_path_pre)
    file_path = r"data\resource_packs"
    name_past = "_x64__8wekyb3d8bbwe"
    if beta:
        name_pre = "Microsoft.MinecraftWindowsBeta_"
    else:
        name_pre = "Microsoft.MinecraftUWP_"
    folder_name = None
    for i in find_list:
        if name_pre in i:
            folder_name = i
    if folder_name is None:
        print("未找到文件目录！")
        return None, None
    else:
        folder_path = os.path.join(folder_path_pre, folder_name, file_path)
        version_internal = folder_name.replace(name_pre, "").replace(name_past, "")
        return folder_path, version_internal


def copy(origin_path,
         target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
         target_folder="text"):
    target_folder_path = os.path.join(target_path, target_folder)
    file_names = os.listdir(origin_path)
    if os.path.isdir(target_folder_path):
        shutil.rmtree(target_folder_path)
    else:
        os.makedirs(target_folder_path)
    for file_name in file_names:
        en_lang = os.path.join(origin_path, file_name, r"texts\en_US.lang")
        zh_lang = os.path.join(origin_path, file_name, r"texts\zh_CN.lang")
        en_exist = os.path.isfile(en_lang)
        zh_exist = os.path.isfile(zh_lang)
        if not (en_exist or zh_exist):
            continue
        else:
            subfolder_path = os.path.join(target_folder_path, file_name)
            os.makedirs(subfolder_path)
            if en_exist:
                shutil.copy(en_lang, subfolder_path)
            if zh_exist:
                shutil.copy(zh_lang, subfolder_path)


def trans_ver(version_internal, beta=True):
    ver = version_internal.split(".")
    ver_1 = int(ver[0])
    ver_2 = int(ver[1])
    ver_combine = int(ver[2])
    ver_3 = ver_combine // 100
    ver_4 = ver_combine % 100
    ver = [ver_1, ver_2, ver_3, ver_4]
    if beta:
        version = str(ver_1) + "." + str(ver_2) + "." + str(ver_3) + "." + str(ver_4)
    else:
        version = str(ver_1) + "." + str(ver_2) + "." + str(ver_3) + " release"
    return version, ver


def readme(version, target_path):
    readme_path = os.path.join(target_path, "README.md")
    if not os.path.exists(readme_path):
        print("未找到 README.md，已跳过相关操作")
        return
    with open(readme_path, "r") as f:
        line = f.readlines()
        f.close()
    line[1] = f"Version: {version}"
    with open(readme_path, "w") as f:
        f.writelines(line)
        f.close()


def read_info(beta, path, append=None, pre=False):
    if append is not None:
        path = os.path.join(path, append)
    if beta and not pre:
        name = 'Preview'
    elif beta and pre:
        name = 'Pre-release'
    else:
        name = 'Release'
    path = os.path.join(path, name)
    if os.path.isfile(path):
        with open(path, 'rb+') as f:
            ver = pickle.load(f)
            f.close()
    else:
        ver = [0, 0, 0, 0]
    return ver


def compare_ver(ver1, ver2):
    flag1 = None
    for i in range(4):
        if ver1[i] > ver2[i]:
            flag1 = True
            break

        elif ver1[i] < ver2[i]:
            flag1 = False
            break

        else:
            i += 1
            continue
    if i < 3:
        flag2 = True
    else:
        flag2 = False
    return flag1, flag2


def update_info(beta, path, ver=None, append=None, pre=False):
    if append is not None:
        path = os.path.join(path, append)
    if beta and not pre:
        name = 'Preview'
    elif beta and pre:
        name = 'Pre-release'
    else:
        name = 'Release'
    path = os.path.join(path, name)
    with open(path, 'wb') as f:
        pickle.dump(ver, f)
        f.close()


def update_lang(beta=True,
                target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test"):
    fd_path, version_in = find(beta)
    if fd_path is None:
        return
    version = trans_ver(version_in, beta)
    print(version)
    copy(fd_path, target_path, "text")
    readme(version, target_path)

## update_info(True, r"D:\Users\Economy\git\Gitee\MCBE-lang", [1, 20, 0, 25], 'object', pre=True)
