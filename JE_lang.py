import os
import json
import zipfile
import pickle
from trivial import get_url


def find_je_lang(game_path=r"E:\Minecraft\.minecraft", target_path=r"D:\Users\Economy\git\Gitee\MCJE-lang"):
    def get_je_ver():
        page = get_url('https://piston-meta.mojang.com/mc/game/version_manifest.json', 100)
        if page is None:
            f = open(r"D:\Users\Economy\git\Gitee\MCJE-lang\ver", 'rb')
            ver = pickle.load(f)
            f.close()
        else:
            ver = page.json()['versions'][0]['id']
            f = open(r"D:\Users\Economy\git\Gitee\MCJE-lang\ver", 'wb')
            pickle.dump(ver, f)
            f.close()
        return ver

    def find_en_us(path):
        ver = get_je_ver()
        print("最新版本:", ver)
        jar_path = os.path.join(path, "versions", ver, ver + ".jar")
        if not os.path.isfile(jar_path):
            print("似乎没有下载游戏资源", os.path.isfile(jar_path))
            return None
        with zipfile.ZipFile(jar_path) as jar:
            with jar.open("assets/minecraft/lang/en_us.json") as f:
                lang = json.load(f)
        return lang

    def find_zh_cn(path):
        assets_path = os.path.join(path, r"assets")
        indexes_path = os.path.join(assets_path, r"indexes")
        index_num = 0
        for i in os.listdir(indexes_path):
            num = int(i.replace(".json", ''))
            if num > index_num:
                index_num = num
        indexes_path = os.path.join(indexes_path, str(index_num) + ".json")
        with open(indexes_path, 'r', encoding='utf-8') as f:
            zh_cn_name = json.load(f)['objects']['minecraft/lang/zh_cn.json']['hash']
        zh_cn_folder = zh_cn_name[0:2]
        zh_cn_path = os.path.join(assets_path, 'objects', zh_cn_folder, zh_cn_name)
        with open(zh_cn_path, 'r', encoding='utf-8') as f:
            zh_cn_lang = json.load(f)
        return zh_cn_lang

    en_us_lang = find_en_us(game_path)
    if en_us_lang is None:
        return
    # create_lang(en_us_lang, target_path, "en_us.lang")

    zh_cn_lang = find_zh_cn(game_path)
    # create_lang(zh_cn_lang, target_path, "zh_cn.lang")
    return en_us_lang, zh_cn_lang


def create_lang(lang, path, name):
    file_path = os.path.join(path, name)
    with open(file_path, 'w', encoding='utf-8') as f:
        for key in lang:
            line = key + 'REPLACE' + repr(lang[key]) + 'REPLACE'
            if "REPLACE'" in line:
                line = line.replace("REPLACE'", '\t').replace("'REPLACE", '\n')
            elif "REPLACE\"" in line:
                line = line.replace("REPLACE\"", '\t').replace("\"REPLACE", '\n')
            f.writelines(line)


# en_us, zh_cn = find_je_lang()

