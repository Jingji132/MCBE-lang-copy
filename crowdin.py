import os.path

import crowdin_api
import json
import requests
import crowdin_api.exceptions
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import BranchPatchPath
from crowdin_api.api_resources.source_files.types import BranchPatchRequest
from crowdin_api.api_resources.source_strings.enums import SourceStringsPatchPath
from crowdin_api.api_resources.source_strings.resource import SourceStringsResource
from crowdin_api.api_resources.source_strings.types import SourceStringsPatchRequest


# 读取配置文件
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
            add_file()
            print('无文件，已自动添加')
            file_dict = get_file()
        file_id = file_dict[version_type]
        print("crowdin分支初始化完成\n当前版本类型：", version_type, "\tbranch_id:", branch_id, "\tfile_id:", file_id)
    else:
        print("版本类型有误！")
        return False
    return True


def update_file():
    # 45/41/11 : Pre-Release/Release/Preview
    storage = client.storages.add_storage(open(file_name, 'rb'))
    # print(file_id, file_name)
    client.source_files.update_file(file_id, storage['data']['id'])
    print("更新完成！")


def add_file():
    # 45/41/11 : Pre-Release/Release/Preview
    storage = client.storages.add_storage(open(file_name, 'rb'))
    # print(file_name)
    client.source_files.add_file(storage['data']['id'], 'processed.csv', branchId=branch_id)
    # ------------------------csv-----------------------------
    # print(my_file)
    print('添加完成')


def del_file():
    # 45/41/11 : Pre-Release/Release/Preview
    client.source_files.delete_file(file_id)
    print('删除完成')
    # print(my_file)


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


def new_branch(branch_name='new_branch'):
    # 新分支的名称
    try:
        branch = client.source_files.add_branch(name=branch_name)
        branch_id_ = branch['data']['id']
        print(f"分支 {branch_name} 添加成功，ID: {branch_id_}")
        return branch_id_
    except crowdin_api.exceptions.APIException as e:
        print(f"添加分支失败: {str(e)}")
        return None


def delete_branch(branch_name='new_branch'):
    def del_branch(branch_id_d):
        try:
            client.source_files.delete_branch(branch_id_d)
            print(f"分支 {branch_id_d} 删除成功")
        except crowdin_api.exceptions.APIException as e:
            print(f"删除分支失败: {str(e)}")

    branch_dict = get_branch()
    if branch_name in branch_dict:
        del_branch(branch_dict['new_branch'])
    else:
        print(f"删除分支失败: '{branch_name}'不存在")


# file()
# Preview/Release/Pre-Release
# init('Pre-Release')
# file()
# new_branch(branch_name=f"Preview()")
def rename_branch(branch_id_r, new_branch_name='new_branch_name'):
    # 重命名分支
    try:
        patch_request = BranchPatchRequest(op=PatchOperation.REPLACE, path=BranchPatchPath.NAME, value=new_branch_name)
        client.source_files.edit_branch(branchId=branch_id_r, data=[patch_request])
        print(f"重命名成功")
    except crowdin_api.exceptions.APIException as e:
        print(f"重命名失败: {str(e)}")


def update_branch(branch, version=None, reset=False):
    # branch:'Preview'/'Release'/'Pre-Release'
    # 初始化
    init_success = init(branch)
    if not init_success:
        return

    # 查找待更新分支
    if version is not None:
        new_name = f"{branch} ({version})"
        print('将重命名为：', new_name)

        # 更新分支
        rename_branch(branch_id, new_name)
    if not reset:
        update_file()
    else:
        del_file()
        add_file()


def download_translate(pre=True):
    if pre:
        ver = 'Pre-Release'
    else:
        ver = 'Release'
    init(version_type=ver)
    response = client.translations.build_project_file_translation(file_id, targetLanguageId='zh-CN')
    client.translations.list_project_builds()
    file_path = fr"D:\Users\Economy\git\Gitee\{git_re}\{ver}\zh-CN"
    file_p = fr"{file_path}\processed.csv"
    # ------------------------csv-----------------------------
    print(response)
    # 下载链接
    download_url = response['data']['url']
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    # 发起下载请求
    response = requests.get(download_url)

    # 检查响应状态码
    if response.status_code == 200:
        # 保存文件
        with open(file_p, "wb+") as file:
            file.write(response.content)

        print("文件已下载并保存")
    else:
        print("下载文件失败")


# update()
# new_branch()
# branch_dict = get_branch()
# rename_branch(53, 'new Thing')
# get_branch()
# add_file(39)
# update_branch('Release', '1.20.0', reset=True)
# new_preview(version='1.20.10.24')
# get_branch()
# init(version_type='Pre-Release')
# a = client.translations.build_project_file_translation(project_id, file_id, targetLanguageId='zh-CN')
# # a = client.translations.list_project_builds(project_id, branchId=43)  # Pre-Release 43
# print(a)
# b = a['data'][0]['data']['id']
# print(b)
# print(b)
# c = client.translations.download_project_translations(project_id, buildId=b)
# print(c)
# print(client.languages.list_supported_languages())

# download_translate()

t = ''
config = f"config{t}.json"
git_re = f'lang-crowdin{t}'
with open(rf"D:\Users\Economy\git\Gitee\mcbe-lang-copy\{config}", "r") as config_file:  # config.json
    config_data = json.load(config_file)
token = config_data["token"]
project_id = config_data["project_id"]
client = crowdin_api.CrowdinClient(token=token, project_id=project_id)

file_id = 0
branch_id = 0
file_name = "None"  # r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.json"

# def test_string():
# strings = client.source_strings.list_strings(fileId=file_id)
# for k in strings:
#     print(k)  # data pagination
# for i in strings['data']:
#     print(i)
# print(i["identifier"])
# edit_request = SourceStringsPatchRequest(
#     op=PatchOperation.,
#     path=SourceStringsPatchPath.TEXT,
#     value='新的字符串内容'
# )
#
# client.source_strings.edit_string(stringId=319521, data=edit_request)


if __name__ == '__main__':
    v_name = ['Preview', 'Pre-Release', 'Release']
    v_n = v_name[0]  # 0 1 2
    # init(v_n, False)
    # test_string()
    update_branch(v_n, reset=False)
    # init('Release')
    # print(client.translations.build_project_file_translation(file_id, targetLanguageId='zh-CN'))
