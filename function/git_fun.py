import os
import pickle

from git import Repo, InvalidGitRepositoryError, GitCommandError

from . import base_fun
# import base_fun
global repo, git_init

def init_repo(repo_path):
    """初始化一个新的Git仓库"""
    # 确保目录存在
    base_fun.make_dir(repo_path)

    # 初始化仓库
    rp = Repo.init(repo_path)
    readme = os.path.join(repo_path, "README.md")
    with open(readme, 'w+') as f:
        f.write("# Language files in Minecraft BE(en_US/zh_CN)\nVersion: 0.0.0")

    rp.git.add('.')
    rp.index.commit("Initial commit")
    print(f"已创建初始提交")

    print(f"已初始化新仓库: {repo_path}")
    return rp


def switch(repo_path, new_branch):
    global repo, git_init
    git_init = False
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        # 仓库不存在，初始化
        print(f"仓库不存在，正在初始化: {repo_path}")
        repo = init_repo(repo_path)
        git_init = True
    except Exception as e:
        print(f"git仓库路径有误，且未初始化：{str(e)}")
        return None
    try:
        repo.git.checkout(new_branch)
    except Exception as e:
        print(f"不存在分支：{new_branch}\n{str(e)}")
        try:
            # 创建新分支（基于当前HEAD）
            print(f"正在创建分支: {new_branch}")
            new_branch_obj = repo.create_head(new_branch)
            new_branch_obj.checkout()
            print(f"已创建并切换到分支: {new_branch}")
            return True
        except Exception as create_error:
            print(f"创建分支失败: {create_error}")
            return None
    return True


def commit(repo_path, file_path='.', commit_message='Update'):
    """
    提交操作
    repo_path = '/path/to/repository'
    file_path = '/path/to/file.txt'
    commit_message = 'Commit message'
    """
    try:
        repo = Repo(repo_path)

        # 添加文件到暂存区
        repo.git.add([file_path])

        # 提交更改
        repo.index.commit(commit_message)

        print("Commit successful.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def diff(repo_path=r"D:\Users\Economy\git\Gitee\MCBE-lang", branch_name='Preview'):
    """
    获取简略差异
    :param repo_path: 仓库路径
    :param branch_name: 分支名
    :return: 差异列表，每个元素为 [change_type, a_path, b_path]，错误时返回空列表
    """
    diff_list = []
    print(repo_path)

    try:
        repo = Repo(repo_path)

        # 检查分支是否存在
        if branch_name not in [b.name for b in repo.branches]:
            print(f"Branch '{branch_name}' not found in the repository.")
            return diff_list  # 返回空列表而不是None

        branch = repo.branches[branch_name]
        commit_ = branch.commit

        # 获取父提交
        if not commit_.parents:
            print("The branch does not have a parent commit.")
            return diff_list

        parent_commit = commit_.parents[0]
        diff_ = parent_commit.diff(commit_)

        # 收集差异信息
        for change in diff_:
            diff_list.append([
                change.change_type,
                change.a_path,
                change.b_path
            ])

    except Exception as e:
        print(f"Error occurred: {str(e)}")

    return diff_list


def diff_info(list_new, ver, path=r"D:\Users\Economy\git\Gitee\MCBE-lang\object\diff_info"):
    if os.path.isfile(path):
        with open(path, 'rb+') as f:
            info = pickle.load(f)
            f.close()
        if 'ver' in info:
            ver_old = info['ver']
            if base_fun.compare_ver(ver, ver_old, complex_return=False):
                info = {'ver': ver, 'list': list_new}
                with open(path, 'wb') as f:
                    pickle.dump(info, f) # type: ignore
                    f.close()
            return info['list']
        else:
            print("diff_info: Format incorrect")
    else:
        info = {'ver': ver, 'list': list_new}
        with open(path, 'wb') as f:
            pickle.dump(info, f)  # type: ignore
            f.close()
        return info['list']

def edit_diff_info(ver, path=r"D:\Users\Economy\git\Gitee\MCBE-lang\object\diff_info"):
    if os.path.isfile(path):
        with open(path, 'rb+') as f:
            info = pickle.load(f)
            f.close()
        print(info)
        # if 'ver' in info:
        #     info['ver'] = ver
        #     with open(path, 'wb') as f:
        #         pickle.dump(info, f) # type: ignore
        #         f.close()
        #     print(info)
            # ver_old = info['ver']
        #     if base_fun.compare_ver(ver, ver_old, complex_return=False):
        #         info = {'ver': ver, 'list': list_new}
        #         with open(path, 'wb') as f:
        #             pickle.dump(info, f) # type: ignore
        #             f.close()
        #     return info['list']
        # else:
        #     print("diff_info: Format incorrect")
    else:
        print("diff_info: Not found")

def tag(repo_path, tag_name):
    """
    获取当前分支的最新提交哈希值
    :param repo_path: 仓库路径
    :return: 当前提交的哈希值
    """
    repo = Repo(repo_path)
    if repo.head.is_detached:
        # 如果当前是分离头状态，直接获取当前提交的哈希值
        _commit = repo.head.commit
    else:
        # 如果当前在分支上，获取分支的最新提交哈希值
        _commit = repo.head.ref.commit
    # tag_name = 'version-test'
    try:
        repo.create_tag(tag_name, _commit, message=tag_name)
    except GitCommandError as e:
        print('git标签出错，已跳过')
        pass


# def pre_tag(repo_path, _target_branch, ver):
#     """
#     将PR版本打标签
#     :param repo_path: 仓库路径
#     :param _target_branch: 目标分支名称
#     :param ver: 新提交的版本号（用于提交信息和标签）
#     """
#     _ver_l = base_fun.ver_str(ver)
#     _ver_s = base_fun.ver_str(ver, False)
#
#     repo = Repo(repo_path)
#     if repo.bare:
#         raise ValueError("仓库无效")
#
#     commit_hash = repo.tags[_ver_l].commit.hexsha
#
#     # 切换到目标分支
#     repo.git.checkout(_target_branch)
#
#     repo.git.merge("--squash", commit_hash)
#     commit_message = _ver_l
#     # repo.git.rebase("--skip")
#     repo.git.commit("-m", commit_message)
#
#     # 创建标签
#     new_tag_name = f"{_ver_s}-pre"
#     repo.create_tag(new_tag_name, message=commit_message)
#
#     print(f"提交已压缩并合并到 {_target_branch}，新标签 {new_tag_name} 已创建")

def pre_tag(repo_path, ver):
    """
    将 PR 版本（已存在标签）压缩合并到目标分支，并打一个 -pre 标签
    :param repo_path: 仓库路径
    :param target_branch: 要合并进去的分支
    :param ver: 版本号元组/列表，如 (1,21,110,26)
    """
    ver_long  = base_fun.ver_str_dis(ver)        # 26.110.26
    ver_short = base_fun.ver_str_dis(ver, False) # 26.110

    repo = Repo(repo_path)
    try:
        repo.create_tag(f"{ver_short}-pre", ref=ver_long)
        print(f"新标签 {ver_short}-pre 已创建")
    except GitCommandError as e:
        print('git标签出错，已跳过')
        pass


if __name__ == '__main__':
    # pre_tag(r"D:\Users\Economy\git\Gitee\MCBE-lang", "Preview", [1,21,110,26])
    # print(diff())
    edit_diff_info( [1,26,0,0])

# commit(r"D:\Users\Economy\git\Gitee\mcbe-lang-copy", '.', 'Update')
# target_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
# switch(target_path, 'Release')


# path1 = r"D:\Users\Economy\git\Gitee\MCBE-lang\object\diff_info"
# info1 = {'ver': [0, 0, 0, 0], 'list': []}
# with open(path1, 'wb') as f:
#     pickle.dump(info1, f)
#     f.close()
# print(diff_info([0,0,0,0,'shw22w222'], [0,1,0,101]))
# with open(path1, 'rb+') as f:
#     info1 = pickle.load(f)
#     f.close()
# print(info1)
