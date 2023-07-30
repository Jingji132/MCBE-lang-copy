
import Update_Lang
import Produce_Lang

import Generate_Template
import Process_json

import trivial
import git_fun
import crowdin


def update_mc_lang(target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", beta=True, mod=False):
    # 找文件位置与版本信息
    fd_path, version_in = Update_Lang.find(beta)
    if fd_path is None:
        return
    version, ver = Update_Lang.trans_ver(version_in, beta)
    print("游戏版本：", version, "\n")
    ver_old = Update_Lang.read_info(beta, target_path, 'object')
    print(ver_old)
    compare, major = Update_Lang.compare_ver(ver, ver_old)

    # git切换分支
    if beta:
        version_type = "Preview"
    else:
        version_type = "Release"
    git_fun.switch(target_path, version_type)

    # 复制文件
    Update_Lang.copy(fd_path, target_path, "text")

    # 更新Readme
    Update_Lang.readme(version, target_path)

    # git提交
    git_fun.commit(target_path, commit_message=version)

    # 更新tips序号
    trivial.update_custom_tips(target_path)

    # 修改模板（排序、名称等）
    template = Generate_Template.update(target_path, path_append_list=["other"])
    if mod:
        Generate_Template.modify(target_path)
        template = Generate_Template.read(target_path)

    # 生成处理文件
    merged_file = f"{version}_merged.lang"
    Produce_Lang.save(template, path=target_path, path_append="other", file_name=merged_file)
    Produce_Lang.process(merged_file, f"{version}_processed.lang", f"{version}_onlykey.lang",
                         path=target_path, path_append="other")

    # 判断预发布版情况（Pre-release）
    preview_reset = False
    if beta:
        diff_list = git_fun.diff()
        print(diff_list)
        json_path = r"D:\Users\Economy\git\Gitee\lang-crowdin\Pre-Release\processed.json"
        ver_pre = Update_Lang.read_info(beta, target_path, 'object', pre=True)
        version_pre = None
        # print(trivial.only_zh_upd(diff_list) and Update_Lang.compare_ver(ver, ver_pre, complex_return=False))
        if trivial.only_zh_upd(diff_list):
            print("未更新英文文件，该版本视为预发布版")
            ver_pre = ver
            version_pre = version
        elif major:
            print("出现跨版本更新，上一版本视为预发布版")
            ver_pre = ver_old
            version_pre = Update_Lang.version(ver_old)

        if version_pre is not None:
            Update_Lang.update_info(beta, target_path, ver_pre, 'object', pre=True)
            Process_json.process_en_json(f"{version_pre}_processed.lang", path=target_path, path_append="other",
                                         json_path=json_path)
            crowdin.update_branch("Pre-Release", version_pre, reset=False)
            preview_reset = True

    # 更新Crowdin
    Process_json.process_en_json(f"{version}_processed.lang", path=target_path, path_append="other",
                                 json_path=rf"D:\Users\Economy\git\Gitee\lang-crowdin\{version_type}\processed.json")
    crowdin.update_branch(version_type, version, reset=preview_reset)

    # 更新版本信息
    # upd_success = input("更新版本号？(Y/N)")
    if compare:
        Update_Lang.update_info(beta, target_path, ver, 'object')


target_path=r"D:\Users\Economy\git\Gitee\MCBE-lang"
update_mc_lang(target_path=r"D:\Users\Economy\git\Gitee\MCBE-lang",  # 提取语言文件至该路径
               # beta=False,  # True:将提取Preview  False:将提取Release
               mod=True  # 是否修改模板
               )

# Update_Lang.update_info(True, target_path, [1, 20, 10, 24], 'object')
