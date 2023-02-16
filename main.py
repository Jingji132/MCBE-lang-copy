import os
import shutil


def copy_lang(version, beta=True):
    floder_path_pre = r"C:\Program Files\WindowsApps"
    if beta:
        folder_name = f'Microsoft.MinecraftWindowsBeta_{Version}_x64__8wekyb3d8bbwe'
    else:
        folder_name = f'Microsoft.MinecraftUWP_{Version}_x64__8wekyb3d8bbwe'
    file_path = r"data\resource_packs"
    folder_path = os.path.join(floder_path_pre, folder_name, file_path)
    file_names = os.listdir(folder_path)
    target_path = r"D:\Users\Economy\Documents\Gitee\MCBE-lang_test"
    for file_name in file_names:
        en_lang = os.path.join(folder_path, file_name, r"texts\en_US.lang")
        zh_lang = os.path.join(folder_path, file_name, r"texts\zh_CN.lang")
        target_folder = os.path.join(target_path, file_name)
        en_exist = os.path.isfile(en_lang)
        zh_exist = os.path.isfile(zh_lang)
        if os.path.exists(target_folder) is False and (en_exist or zh_exist):
            os.mkdir(target_folder)
        if en_exist:
            shutil.copy(en_lang, target_folder)
        if zh_exist:
            shutil.copy(zh_lang, target_folder)


copy_lang(version='1.19.7023.0', beta=True)

