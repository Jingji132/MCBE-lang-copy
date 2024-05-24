import os
import pickle

from git import Repo

import Update_Lang


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
            if Update_Lang.compare_ver(ver, ver_old, complex_return=False):
                info = {'ver': ver, 'list': list_new}
                with open(path, 'wb') as f:
                    pickle.dump(info, f)
                    f.close()
            return info['list']
        else:
            print("diff_info: Format incorrect")
    else:
        print("diff_info: Not found")


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
