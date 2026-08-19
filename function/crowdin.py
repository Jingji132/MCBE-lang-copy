import json
import os
import urllib3
import requests
import crowdin_api
import crowdin_api.exceptions
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import BranchPatchPath
from crowdin_api.api_resources.source_files.types import BranchPatchRequest

from . import base_fun

# 全局变量初始化
file_id = 0
branch_id = 0
csv_name = "None"
file_name = "None"


# ==================== 核心逻辑函数 ====================
def init(version_type='Preview', csv=True):
    """初始化 Crowdin 分支与文件配置，具备网络异常拦截功能"""
    global file_name, file_id, branch_id
    file_name = fr"{csv_name}\{version_type}\processed.csv"
    print(csv_name, version_type, file_name)

    # 1. 获取远程分支字典
    branch_dict = get_branch()
    if not branch_dict:
        print("❌ 错误：未能获取到任何 Crowdin 远程分支，请检查网络连接或代理设置！")
        return False

    # 2. 获取远程文件字典
    file_dict = get_file(csv)
    if not file_dict:  # 现在 get_file 保证返回字典，不会为 None
        print("❌ 错误：未能获取到 Crowdin 远程文件列表，请检查网络连接！")
        return False

    # 3. 校验目标分支是否存在
    if version_type not in branch_dict:
        print(f"❌ 错误：在 Crowdin 远程仓库中未找到名为 '{version_type}' 的基础分支！")
        print(f"当前云端可用分支: {list(branch_dict.keys())}")
        return False

    branch_id = branch_dict[version_type]
    ver_list = ['Preview', 'Pre-Release', 'Release']

    if version_type in ver_list:
        if version_type not in file_dict:
            add_file()
            print('⚠️ 未在云端分支找到对应文件，已执行自动创建...')
            file_dict = get_file(csv)
            if not file_dict or version_type not in file_dict:
                print("❌ 错误：自动创建文件后仍无法解析出有效的 file_id！")
                return False

        file_id = file_dict[version_type]
        print(f"✅ Crowdin 分支初始化成功！\n    当前版本类型: {version_type} | branch_id: {branch_id} | file_id: {file_id}")
    else:
        print("❌ 错误：传入的版本类型有误！可选范围：['Preview', 'Pre-Release', 'Release']")
        return False
    return True


def get_branch():
    """从 Crowdin 获取所有分支列表"""
    branch_dict_ = {}
    try:
        project_branches = client.source_files.list_project_branches()
        for i in project_branches['data']:
            # 提取括号前的标准名字，如 "Preview (1.21.40)" -> "Preview"
            name_key = i['data']['name'].split(' (')[0]
            branch_dict_[name_key] = i['data']['id']
        print("【当前云端分支映射】", branch_dict_)
    except Exception as e:
        print(f"❌ 获取云端分支失败 (网络异常): {str(e)}")
        return {}  # 发生异常时显式返回空字典，防止上游引发 KeyError
    return branch_dict_


def get_file(csv=True):
    """从 Crowdin 获取指定格式的文件列表"""
    fm = 'csv' if csv else 'json'
    try:
        project_files = client.source_files.list_files()
        file_dict_ = {}
        for f in project_files['data']:
            if f['data']['name'] == f'processed.{fm}':
                file_id_ = f['data']['id']
                path_parts = f['data']['path'].split('/')
                # 增加防御性切片保护，防止深层路径切片越界
                if len(path_parts) > 1:
                    file_type_ = path_parts[1].split(' (')[0]
                    file_dict_[file_type_] = file_id_
        print("【当前云端文件映射】", file_dict_)
        return file_dict_
    except Exception as e:
        print(f"❌ 获取云端文件失败 (网络异常): {str(e)}")
        return {}  # ✨ 核心修复：显式返回空字典，避免隐式返回 None 导致 isinstance 报错


# ==================== 文件与分支操作函数 ====================

def update_file():
    """更新云端已有文件内容"""
    storage = client.storages.add_storage(open(file_name, 'rb'))
    client.source_files.update_file(file_id, storage['data']['id'])
    print("🚀 文件内容更新同步完成！")


def reset_file():
    """使用预设模板重置云端文件"""
    reset_file_name = fr"D:\Documents\GitHub\{git_re}\preset\processed.csv"
    storage = client.storages.add_storage(open(reset_file_name, 'rb'))
    client.source_files.update_file(file_id, storage['data']['id'])
    print("🔄 文件初始化重置完成！")


def add_file():
    """向当前分支推送新文件"""
    storage = client.storages.add_storage(open(file_name, 'rb'))
    client.source_files.add_file(storage['data']['id'], 'processed.csv', branchId=branch_id)
    print('➕ 新文件成功挂载至目标分支')


def del_file():
    """删除云端当前文件"""
    client.source_files.delete_file(file_id)
    print('🗑️ 文件删除成功')


def new_branch(branch_name='new_branch'):
    """新建云端分支"""
    try:
        branch = client.source_files.add_branch(name=branch_name)
        branch_id_ = branch['data']['id']
        print(f"✨ 分支 {branch_name} 创建成功，ID: {branch_id_}")
        return branch_id_
    except crowdin_api.exceptions.APIException as e:
        print(f"❌ 创建分支失败: {str(e)}")
        return None


def delete_branch(branch_name='new_branch'):
    """按名字删除云端分支"""

    def del_branch(branch_id_d):
        try:
            client.source_files.delete_branch(branch_id_d)
            print(f"🗑️ 分支 ID: {branch_id_d} 销毁成功")
        except crowdin_api.exceptions.APIException as e:
            print(f"❌ 销毁分支失败: {str(e)}")

    branch_dict = get_branch()
    if branch_name in branch_dict:
        del_branch(branch_dict[branch_name])
    else:
        print(f"❌ 操作失败：目标分支 '{branch_name}' 在云端不存在")


def rename_branch(branch_id_r, new_branch_name='new_branch_name'):
    """重命名指定的云端分支"""
    try:
        patch_request = BranchPatchRequest(op=PatchOperation.REPLACE, path=BranchPatchPath.NAME, value=new_branch_name)
        client.source_files.edit_branch(branchId=branch_id_r, data=[patch_request])
        print(f"📝 分支重命名成功 -> {new_branch_name}")
        return True
    except Exception as e:
        print(f"❌ 分支重命名失败: {str(e)}")
        return False


def update_branch(branch, version=None, reset=False):
    """主入口：更新分支名称并推送最新翻译文本（带全面的返回值保护）"""
    init_success = init(branch)
    if not init_success:
        print("🛑 鉴于初始化未能正常完成，后续推送任务自动挂起。")
        return False

    if version is not None:
        new_name = f"{branch} ({version})"
        print('⚡ 即将重命名分支为：', new_name)
        # 如果重命名失败，可以记录但不一定中断，根据需求这里选择继续推送
        rename_branch(branch_id, new_name)

    # ✨ 核心改进：捕获核心上传流程中的网络异常，防止上传失败却误以为成功
    try:
        if not reset:
            update_file()
        else:
            reset_file()
            update_file()
        return True
    except Exception as e:
        print(f"❌ 文件同步推送失败 (网络中断或API内部限制): {str(e)}")
        return False


def download_translate(pre=True):
    """下载 Crowdin 云端最新的简繁体本地化翻译文件"""
    ver = 'Pre-Release' if pre else 'Release'
    if not init(version_type=ver):
        return

    response_zh_cn = client.translations.build_project_file_translation(file_id, targetLanguageId='zh-CN')
    response_zh_tw = client.translations.build_project_file_translation(file_id, targetLanguageId='zh-TW')
    client.translations.list_project_builds()

    file_path = fr"D:\Documents\GitHub\{git_re}\{ver}\download"
    file_zh_cn = fr"{file_path}\zh_CN.csv"
    file_zh_tw = fr"{file_path}\zh_TW.csv"
    base_fun.make_dir(file_path)

    response_zh_cn = requests.get(response_zh_cn['data']['url'])
    response_zh_tw = requests.get(response_zh_tw['data']['url'])

    def download_csv(response, file):
        if response.status_code == 200:
            with open(file, "wb+") as f:
                f.write(response.content)
            print(f"⬇️ 成功同步：{file}")
        else:
            print(f"❌ 链路请求失败，{file} 下载未响应")

    download_csv(response_zh_cn, file_zh_cn)
    download_csv(response_zh_tw, file_zh_tw)


# ==================== 客户端环境初始化 ====================

t = ''
config = f"config{t}.json"
git_re = f'lang-crowdin{t}'

def socket_check_proxy(host="127.0.0.1", port=7890, timeout=1.0):
    """探测本地代理端口是否开放"""
    import socket
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, socket.timeout):
        return False

# 🌟 自动检测代理状态
PROXY_PORT = 7890

if socket_check_proxy(port=PROXY_PORT):
    print(f"📡 [网络提示] 检测到本地代理端口 {PROXY_PORT} 已开放，已自动启用代理隧道。")
    os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{PROXY_PORT}'
    os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{PROXY_PORT}'
else:
    print(f"🌐 [网络提示] 未检测到代理软件响应（端口 {PROXY_PORT} 积极拒绝）。已自动切换为【本地直连/裸连】模式。")
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)

# 消除不安全证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def init_conf(token, id):
    global client
    # 创建唯一的 API 客户端实例
    client = crowdin_api.CrowdinClient(token=token, project_id=id, timeout=240)

global client

if __name__ == '__main__':
    # 测试主入口
    update_branch('Preview', '1.21.120.20', reset=True)