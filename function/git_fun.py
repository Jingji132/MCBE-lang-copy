import os
import pickle

from git import Repo

from . import base_fun


def switch(repo_path, new_branch):
    repo = Repo(repo_path)
    try:
        repo.git.checkout(new_branch)
    except Exception as e:
        print(f"不存在分支：{new_branch}\n{str(e)}")


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
    :param repo_path:
    :param branch_name:
    :return:
    """
    try:
        repo = Repo(repo_path)
        branch = repo.branches[branch_name]
        diff_list = []

        if branch:
            commit_ = branch.commit
            parent_commit = commit_.parents[0] if commit_.parents else None

            if parent_commit:
                diff_ = parent_commit.diff(commit_)

                for change in diff_:
                    diff_list.append([change.change_type, change.a_path, change.b_path])
            else:
                print("The branch does not have a parent commit.")
                return
        else:
            print("Branch not found in the repository.")
            return
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return
    # print(list)
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
    repo.create_tag(tag_name, _commit, message=tag_name)


def pre_merge(repo_path, _target_branch, ver):
    """
    将指定提交及其之前的提交压缩为一个提交，并合并到目标分支
    :param repo_path: 仓库路径
    :param _target_branch: 目标分支名称
    :param ver: 新提交的版本号（用于提交信息和标签）
    """
    _ver_l = base_fun.ver_str(ver)
    _ver_s = base_fun.ver_str(ver, False)

    repo = Repo(repo_path)
    if repo.bare:
        raise ValueError("仓库无效")

    commit_hash = repo.tags[_ver_l].commit.hexsha

    # 切换到目标分支
    repo.git.checkout(_target_branch)

    # 创建一个新的提交，将指定提交及其之前的提交压缩为一个
    repo.git.merge("--squash", commit_hash)
    commit_message = _ver_l
    repo.git.commit("-m", commit_message)

    # 创建标签
    new_tag_name = f"{_ver_s}-pre"
    repo.create_tag(new_tag_name, message=commit_message)

    print(f"提交已压缩并合并到 {_target_branch}，新标签 {new_tag_name} 已创建")

if __name__ == '__main__':
    print(diff())

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
