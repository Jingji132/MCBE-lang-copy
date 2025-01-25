import os
import crowdin_api
import requests


def make_dir(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)
        return


def get_branch():
    branch_dict_ = {}
    try:
        project_branches = client.source_files.list_project_branches()
        for i in project_branches['data']:
            branch_dict_[i['data']['name'].split(' (')[0]] = i['data']['id']
        print("分支：", branch_dict_)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    return branch_dict_


def get_file(csv=True):
    if csv:
        fm = 'csv'
    else:
        fm = 'json'
    try:
        project_files = client.source_files.list_files()
        file_dict_ = {}
        for f in project_files['data']:
            if f['data']['name'] == f'processed.{fm}':  # 替换成您的 JSON 文件名
                # ------------------------csv-----------------------------
                file_id_ = f['data']['id']
                file_type_ = f['data']['path'].split('/')[1].split(' (')[0]
                # print(f"{file_type_}\tFile ID: {file_id_}")
                file_dict_[file_type_] = file_id_
        print("文件：", file_dict_)
        return file_dict_
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def init(version_type='Preview', csv=True):
    global file_name, file_id, branch_id
    file_name = fr"D:\Users\Economy\git\Gitee\{git_re}\{version_type}\processed.csv"  # lang-crowdin
    # ------------------------csv-----------------------------
    file_dict = get_file(csv)
    branch_dict = get_branch()
    branch_id = branch_dict[version_type]
    ver_list = ['Preview', 'Pre-Release', 'Release']
    if version_type in ver_list:
        if version_type not in file_dict:
            print('无文件')
            return
        file_id = file_dict[version_type]
        print("crowdin分支初始化完成\n当前版本类型：", version_type, "\tbranch_id:", branch_id, "\tfile_id:", file_id)
    else:
        print("版本类型有误！")
        return False
    return True


def download_translate(pre=True, file_path=r"D:\Users\Economy\git\Gitee\download"):
    if pre:
        ver = 'Pre-Release'
    else:
        ver = 'Release'
    init(version_type=ver)
    response_zh_cn = client.translations.build_project_file_translation(file_id, targetLanguageId='zh-CN')
    response_zh_tw = client.translations.build_project_file_translation(file_id, targetLanguageId='zh-TW')
    # client.translations.list_project_builds()
    file_zh_cn = fr"{file_path}\zh_CN.csv"
    file_zh_tw = fr"{file_path}\zh_TW.csv"
    make_dir(file_path)
    # print(response_zh_cn, response_zh_tw)
    # 发起下载请求
    response_zh_cn = requests.get(response_zh_cn['data']['url'])
    response_zh_tw = requests.get(response_zh_tw['data']['url'])

    # print(response_zh_cn)

    def download_csv(response, file):
        if response.status_code == 200:
            with open(file, "wb+") as file:
                file.write(response.content)
            print(f"{file}已下载并保存")
        else:
            print(f"{file}下载失败")

    download_csv(response_zh_cn, file_zh_cn)
    download_csv(response_zh_tw, file_zh_tw)


t = ''
git_re = f'lang-crowdin{t}'
# ——————↓↓↓↓这里是你在crowdin创建的令牌↓↓↓↓——————
token = "19f3c99171f321903a8110340864e16cd08755fb686d3997c999315b9a80ffc305d6e38e2494b306"
# ——————↓↓↓↓这里是你要下载文件的位置↓↓↓↓——————
file_path = r"D:\Users\Economy\I_Dont_Know\download"
project_id = 590029
client = crowdin_api.CrowdinClient(token=token, project_id=project_id)

file_id = 0
branch_id = 0
file_name = "None"  # r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.json"

if __name__ == '__main__':
    pre = True
    download_translate(pre, file_path)
