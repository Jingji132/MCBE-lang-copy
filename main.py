import Update_Lang
import Produce_Lang

import Generate_Template
import Convert_Lang
import base_fun
import debug

import trivial
import git_fun
import crowdin


def update_mc_lang(beta=True,
                   target_path=r"...\MCBE-lang_UPD_test",
                   crowdin_path=r"...\lang-crowdin"):
    # 找文件位置与版本信息
    fd_path, version_in = Update_Lang.find(beta)
    if fd_path is None:
        return
    version, ver = Update_Lang.trans_ver(version_in, beta)
    print("本机安装版本：", ver)
    info_old = Update_Lang.read_info(beta, target_path, 'object')
    if info_old is None:
        debug.lang_init()
        print('未找到版本信息文件（object）,已在目录下创建')
        info_old = Update_Lang.read_info(beta, target_path, 'object')
    ver_old = info_old['ver']
    print("信息记录版本：", ver_old)
    compare, major = base_fun.compare_ver(ver, ver_old, complex_return=True)

    if not compare:
        if ver == ver_old and (not info_old['git'] or not info_old['crowdin']):
            print("有未完成的更新，将继续")
        else:
            print("无需更新！")
            return
    else:
        Update_Lang.update_info(beta, target_path, 'object', ver, git=False, crowdin=False)

    # git切换分支
    if beta:
        version_type = "Preview"
    else:
        version_type = "Release"
    git_fun.switch(target_path, version_type)

    if compare or not info_old['git']:
        # 复制文件
        Update_Lang.copy(fd_path, target_path, "text")

        # 更新Readme
        Update_Lang.readme(version, target_path)

        # git提交
        git_fun.commit(target_path, commit_message=version)

        Update_Lang.update_info(beta, target_path, 'object', git=True)

    # 更新tips序号（目前无需此操作）
    # trivial.update_custom_tips(target_path)

    # 更新模板
    template = Generate_Template.update_json(beta, target_path)

    # 修改模板（已弃用），模板已改为json格式，可手动修改
    # if mod:
    #     Generate_Template.modify(target_path)
    #     template = Generate_Template.read(target_path)

    # 生成处理文件
    merged_file = f"{version}_merged.lang"
    Produce_Lang.save(template, target_path, fr"{target_path}/other/{merged_file}")

    processed_file = f"{version}_processed.lang"
    Produce_Lang.process(fr"{target_path}/other/{merged_file}",
                         fr"{target_path}/other/{processed_file}")

    # 判断预发布版情况（Pre-release）
    if compare or not info_old['crowdin']:
        preview_reset = False
        version_pre = None
        ver_pre = None
        if beta:
            diff_list = git_fun.diff_info(git_fun.diff(), ver)
            print(diff_list)
            info_pre = Update_Lang.read_info(beta, target_path, 'object', pre=True)
            ver_pre = info_pre['ver']
            # print(trivial.only_zh_upd(diff_list) and Update_Lang.compare_ver(ver, ver_pre, complex_return=False))
            if trivial.only_zh_upd(diff_list):
                print("未更新英文文件，该版本视为预发布版")
                if ver_pre == ver and info_pre['crowdin']:
                    print("已更新过，不再更新！")
                else:
                    ver_pre = ver
                    version_pre = version
            elif major:
                print("出现跨版本更新，上一版本视为预发布版")
                if ver_old == ver_pre and info_pre['crowdin']:
                    print("上一板本已是预发布版，并且已更新过，不再更新！")
                else:
                    ver_pre = ver_old
                    version_pre = Update_Lang.version(ver_old)

            if version_pre is not None:
                input(f"将更新预发布版：{version_pre}（输入任意内容以继续）")
                processed_path = rf"{crowdin_path}\Pre-Release\processed.csv"
                Convert_Lang.process_csv(input_path=rf"{target_path}\other\{version_pre}_processed.lang",
                                         output_path=processed_path,
                                         special_key=True)
                trivial.add_bad_translation(template, target_path,
                                            rf"{target_path}\other\{version_pre}_zh_BAD.lang",
                                            processed_path)
                crowdin.update_branch("Pre-Release", version_pre, reset=False)
                preview_reset = True

        # 更新Crowdin
        processed_path = rf"{crowdin_path}\{version_type}\processed.csv"
        Convert_Lang.process_csv(input_path=rf"{target_path}\other\{version}_processed.lang",
                                 output_path=processed_path,
                                 special_key=True)
        trivial.add_bad_translation(template, target_path,
                                    rf"{target_path}\other\{version}_zh_BAD.lang",
                                    processed_path)
        crowdin.update_branch(version_type, version, reset=preview_reset)
        Update_Lang.update_info(beta, target_path, 'object', crowdin=True)

        # 等待Preview更新完成后再将Pre-release标记为更新完成
        if version_pre is not None:
            Update_Lang.update_info(beta, target_path, ver_pre, 'object', pre=True, crowdin=True)

    # 更新版本信息
    # upd_success = input("更新版本号？(Y/N)")
    # if compare:
    #     Update_Lang.update_info(beta, target_path, ver, 'object')


if __name__ == '__main__':
    main_in = None
    main_beta = None
    while True:
        main_in = input("检测更新的版本（0:Preview 1:Release）：")
        if main_in == '0':
            main_beta = True
            break
        elif main_in == '1':
            main_beta = False
            break
        else:
            print('输入有误，请重新输入！')
    # 提取语言文件位置（git位置）
    tg_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    '''
        可选择fork https://github.com/Jingji132/MCBE-lang后将仓库下载至本地，将以上路径设置为仓库路径
    '''
    # csv文件位置（用于上传crowdin）
    csv_path = r"D:\Users\Economy\git\Gitee\lang-crowdin"

    update_mc_lang(target_path=tg_path,  # 提取语言文件至该路径
                   beta=main_beta,  # True:将提取Preview  False:将提取Release
                   # mod=True  # 是否修改模板
                   )

    a = input("请按任意键退出~")

# Update_Lang.update_info(True, target_path, [1, 20, 10, 24], 'object')
