import crowdin_api
import json
import requests
import crowdin_api.exceptions
from crowdin_api.api_resources.enums import PatchOperation, ExportProjectTranslationFormat
from crowdin_api.api_resources.source_files.enums import BranchPatchPath
from crowdin_api.api_resources.source_files.types import BranchPatchRequest

# 读取配置文件
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
token = config_data["token"]
project_id = 590029
file_id = 0
file_name = r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.json"
client = crowdin_api.CrowdinClient(token=token)


def init(version_type='Preview'):
    global file_name, file_id
    file_dict = get_file()
    if version_type in file_dict:
        file_id = file_dict[version_type]
        print("version_type:", version_type, "\nfile_id:", file_id)
    else:
        print("版本类型有误！")
        return False
    file_name = fr"D:\Users\Economy\git\Gitee\lang-crowdin\{version_type}\processed.json"
    return True


def update_file():
    # 45/41/11 : Pre-Release/Release/Preview
    storage = client.storages.add_storage(open(file_name, 'rb'))
    # print(file_id, file_name)
    client.source_files.update_file(project_id, file_id, storage['data']['id'])
    print("更新完成！")


def add_file(branch_id):
    # 45/41/11 : Pre-Release/Release/Preview
    storage = client.storages.add_storage(open(file_name, 'rb'))
    my_file = client.source_files.add_file(project_id, storage['data']['id'], 'processed.json', branchId=branch_id)
    print(my_file)


def del_file(branch_id):
    # 45/41/11 : Pre-Release/Release/Preview
    storage = client.storages.add_storage(open(file_name, 'rb'))
    client.source_files.delete_file(project_id, file_id)
    # print(my_file)


def get_branch():
    branch_dict_ = {}
    try:
        project_branches = client.source_files.list_project_branches(projectId=project_id)
        for i in project_branches['data']:
            branch_dict_[i['data']['name'].split(' (')[0]] = i['data']['id']
        print("branch:", branch_dict_)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    return branch_dict_


def get_file():
    try:
        project_files = client.source_files.list_files(projectId=project_id)
        file_dict_ = {}
        for f in project_files['data']:
            if f['data']['name'] == 'processed.json':  # 替换成您的 JSON 文件名
                file_id_ = f['data']['id']
                file_type_ = f['data']['path'].split('/')[1].split(' (')[0]
                # print(f"{file_type_}\tFile ID: {file_id_}")
                file_dict_[file_type_] = file_id_
        print(file_dict_)
        return file_dict_
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def new_branch(branch_name='new_branch'):
    # 新分支的名称
    try:
        branch = client.source_files.add_branch(project_id, name=branch_name)
        branch_id_ = branch['data']['id']
        print(f"分支 {branch_name} 添加成功，ID: {branch_id_}")
        return branch_id_
    except crowdin_api.exceptions.APIException as e:
        print(f"添加分支失败: {str(e)}")
        return None


def del_branch(branch_id):
    try:
        client.source_files.delete_branch(project_id, branch_id)
        print(f"分支 {branch_id} 删除成功")
    except crowdin_api.exceptions.APIException as e:
        print(f"删除分支失败: {str(e)}")


def delete_branch(branch_name='new_branch'):
    branch_dict_ = get_branch()
    if branch_name in branch_dict_:
        del_branch(branch_dict_['new_branch'])
    else:
        print(f"删除分支失败: '{branch_name}'不存在")


# file()
# Preview/Release/Pre-Release
# init('Pre-Release')
# file()
# new_branch(branch_name=f"Preview()")
def rename_branch(branch_id, new_branch_name='new_branch_name'):
    # 重命名分支
    try:
        patch_request = BranchPatchRequest(op=PatchOperation.REPLACE, path=BranchPatchPath.NAME, value=new_branch_name)
        client.source_files.edit_branch(projectId=project_id, branchId=branch_id, data=[patch_request])
        print(f"重命名成功")
    except crowdin_api.exceptions.APIException as e:
        print(f"重命名失败: {str(e)}")


def update_branch(branch, version, reset=False):
    # branch:'Preview'/'Release'/'Pre-Release'
    # 初始化
    init_success = init(branch)
    if not init_success:
        return
    b_dict = get_branch()

    # 查找待更新分支
    old_name = None
    b_id = None
    for b in b_dict:
        if branch == b:
            old_name = b
            b_id = b_dict[b]
    new_name = f"{branch} ({version})"
    print(old_name, b_id, new_name)

    # 更新分支
    rename_branch(b_id, new_name)
    if not reset:
        update_file()
    else:
        del_file(b_id)
        add_file(b_id)


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
def download_translate():
    init(version_type='Pre-Release')
    response = client.translations.build_project_file_translation(project_id, file_id, targetLanguageId='zh-CN')
    file_path = r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\zh-CN\processed.json"
    print(response)
    # 下载链接
    download_url = response['data']['url']

    # 发起下载请求
    response = requests.get(download_url)

    # 检查响应状态码
    if response.status_code == 200:
        # 保存文件
        with open(file_path, "wb") as file:
            file.write(response.content)

        print("文件已下载并保存")
    else:
        print("下载文件失败")


# print(client.languages.list_supported_languages())

# download_translate()
