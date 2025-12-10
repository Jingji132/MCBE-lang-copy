import os.path
from random import randint
import requests

from .Convert_Lang import lang_to_dict, csv_add_context
from .Produce_Lang import save
from .Update_Lang import update_info


def get_url(url, time_set=200):
    headers = {
        'user-agent': f'Mozilla/5.0 (Linux; Android {randint(6, 14)}; OnePlus {randint(7, 11)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'}
    for timeout in range(time_set, time_set + 3):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            print(f"Request succeeded with timeout: {timeout}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed with timeout: {timeout}, error: {e}")
            continue
    else:
        print("All attempts failed.")
        return None


def only_zh_upd(diff_list):
    for i in diff_list:
        for j in i:
            if 'en_US.lang' in j:
                return False
    return True


def add_bad_translation(template=None,
                        target_path=r"D:\Users\Economy\git\Gitee\MCBE-lang",
                        zh_merged_path=r"D:\Users\Economy\git\Gitee\MCBE-lang\test",
                        csv_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.csv",
                        version = ''):
    for zh_type in ['CN', 'TW']:
        merged_path = os.path.join(zh_merged_path, f"{version}_zh_{zh_type}_BAD.lang")
        save(template, target_path, merged_path, zh=zh_type)
        zh_dict = lang_to_dict(merged_path)
        csv_add_context(zh_dict, csv_path, f'zh_{zh_type}：')


def lang_init(path=r"D:\Users\Economy\git\Gitee\MCBE-lang-test1"):
    # n_path = rf'{path}\object'
    # os.makedirs(n_path)
    for beta in [True, False]:
        for pre in [True, False]:
            # print(beta, pre)
            update_info(beta, path, 'object', pre=pre)
    return

if __name__ == '__main__':
    # target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    # template = Generate_Template.read(target_path)
    # add_bad_translation(template, target_path,
    #                     r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.0.26_zh_BAD.lang",
    #                     r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\processed.csv")

    # crowdin.update_branch('Pre-Release')

    pass
