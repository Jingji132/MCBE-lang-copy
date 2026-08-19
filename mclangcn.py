from function.crowdin import download_translate, init_conf, init
from function.Convert_Lang import csv_to_lang, json_to_lang
from function.Update_Lang import version_str, read_info
from function import config

def crowdin_to_mclangcn_json(_pre=True):
    if _pre:
        ver = 'Pre-'
    else:
        ver = ''
    path1 = fr"D:\Documents\GitHub\lang-crowdin\{ver}Release\zh-CN\processed.json"
    path2 = r"D:\Documents\GitHub\mclangcn\texts\zh_CN.lang"
    version_pre = version_str(read_info(True, r'D:\Documents\GitHub\MCBE-lang\object', pre=True)['ver'])
    print(version_pre)
    path3 = rf"D:\Documents\GitHub\MCBE-lang\other\{version_pre}_processed.lang"

    download_translate()

    json_to_lang(path1, path2, path3)

def crowdin_to_mclangcn_csv(_pre=True, lang_type='zh_CN'):
    if _pre:
        ver = 'Pre-'
    else:
        ver = ''
    path1 = fr"D:\Documents\GitHub\lang-crowdin\{ver}Release\download\{lang_type}.csv"
    path2 = fr"D:\Documents\GitHub\mclangcn\texts\{lang_type}.lang"
    version_v = version_str(read_info(beta=_pre, path=r'D:\Documents\GitHub\MCBE-lang\object', pre=_pre)['ver'])
    if not _pre:
        version_l = version_v.split('.')
        version_v = version_l[0]+'.'+version_l[1]+'.'+version_l[2]+' Release'
    path3 = rf"D:\Documents\GitHub\MCBE-lang\process file\{version_v}_processed.lang"

    csv_to_lang(path1, path2, path3)

if __name__ == '__main__':
    conf = config.init_config(r'config/config.json')
    init_conf(conf.crowdin_token, conf.crowdin_project_id)
    # init()
    pre = True
    download_translate(pre)
    crowdin_to_mclangcn_csv(pre)
    # Convert_Lang.crowdin_to_mclangcn_csv(pre, 'zh_TW')