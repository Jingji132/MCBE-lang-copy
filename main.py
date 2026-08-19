import ctypes
import os
import subprocess
import sys

from function import trivial, Convert_Lang, crowdin, git_fun, Produce_Lang, Update_Lang, Generate_Template, \
    base_fun, config


def run_as_admin():
    """以管理员权限使用 Windows Terminal 重新运行当前脚本"""

    def is_admin():
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        # 1. 获取当前脚本的绝对路径
        script_path = os.path.abspath(sys.argv[0])
        # 2. 获取当前脚本所在的文件夹路径（解决 System32 路径丢失问题）
        current_dir = os.path.dirname(script_path)
        # 3. 获取当前 Python 解释器的绝对路径（解决环境变量找不到 python 的问题）
        python_exe = sys.executable

        # 核心修复：
        # -d "{current_dir}" 让 WT 正确切换到你脚本所在的目录
        # 使用 cmd /k 执行可以完美支持 Python 的 input() 输入交互
        wt_arguments = f'-d "{current_dir}" cmd /k ""{python_exe}" "{script_path}""'

        # 构建 PowerShell 提权命令
        ps_command = f'Start-Process -FilePath "wt.exe" -ArgumentList \'{wt_arguments}\' -Verb RunAs'

        # 执行提权
        subprocess.run(['powershell.exe', '-Command', ps_command], capture_output=True)
        sys.exit()

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
        trivial.lang_init()
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
    if not git_fun.switch(target_path, version_type):
        return

    if compare or not info_old['git']:
        # 复制文件
        Update_Lang.copy(fd_path, target_path, "text")

        # 更新Readme
        Update_Lang.readme(version, target_path)

        # git提交
        git_fun.commit(target_path, commit_message=version)
        git_fun.tag(target_path, tag_name=version)

        Update_Lang.update_info(beta, target_path, 'object', git=True)

    # 更新模板
    template = Generate_Template.update_json(beta, target_path, ver=ver)

    # 生成处理文件
    merged_file = f"{version}_merged.lang"
    Produce_Lang.save(template, target_path, fr"{target_path}/process file/{merged_file}")

    processed_file = f"{version}_processed.lang"
    Produce_Lang.process(fr"{target_path}/process file/{merged_file}",
                         fr"{target_path}/process file/{processed_file}")

    # 判断预发布版情况（Pre-release）
    version_pre = None
    info_pre = Update_Lang.read_info(True, target_path, 'object', pre=True)
    if compare or not info_old['crowdin'] or not info_pre['crowdin']:
        preview_reset = False
        ver_pre = None
        crowdin.csv_name = crowdin_path
        if beta:
            diff_list = git_fun.diff_info(git_fun.diff(target_path), ver, fr"{target_path}\object\diff_info")
            # print(diff_list)
            ver_pre = info_pre['ver']
            # print(trivial.only_zh_upd(diff_list) and Update_Lang.compare_ver(ver, ver_pre, complex_return=False))
            if trivial.only_zh_upd(diff_list):
                print("未更新英文文件，该版本视为预发布版")
                if ver_pre == ver and info_pre['crowdin']:
                    print("已更新过，不再更新！")
                else:
                    ver_pre = ver
                    version_pre = version
                    Update_Lang.update_info(True, target_path, 'object', ver_pre,
                                            pre=True, crowdin=False, git=False)
            elif major:
                print("出现跨版本更新，上一版本视为预发布版")
                if ver_old == ver_pre and info_pre['crowdin']:
                    print("上一板本已是预发布版，并且已更新过，不再更新！")
                else:
                    ver_pre = ver_old
                    # version_pre = Update_Lang.version_str_ini(ver_old)
                    version_pre = base_fun.ver_str_dis(ver_pre)
                    Update_Lang.update_info(True, target_path, 'object', ver_pre,
                                            pre=True, crowdin=False, git=False)

        if version_pre is None and not info_pre['crowdin']:
            ver_pre = info_pre['ver']
            version_pre = base_fun.ver_str_dis(ver_pre)
            print("之前有预发布版未更新，即将更新！")

        if version_pre is not None and ver_pre[0]!=0:
            do_update_pre = input(f"将更新预发布版：{version_pre}（Y继续）")
            if do_update_pre in ['y', 'Y']:
                pass
            else:
                print('更新中断！')
                return
            preview_reset = True

            if not info_pre['git']:
                git_fun.pre_tag(target_path, ver_pre)
                Update_Lang.update_info(beta, target_path, 'object', ver_pre, pre=True, git=True)

            processed_path = rf"{crowdin_path}\Pre-Release\processed.csv"
            Convert_Lang.process_csv(input_path=rf"{target_path}\process file\{version_pre}_processed.lang",
                                     output_path=processed_path,
                                     special_key=True, debug=conf.debug, version=version_pre)
            trivial.add_bad_translation(template, target_path,
                                        rf"{target_path}\process file",
                                        processed_path, version_pre)
            if crowdin.update_branch("Pre-Release", version_pre, reset=False):
                Update_Lang.update_info(beta, target_path, 'object', ver_pre, pre=True, crowdin=True)

        # 更新Crowdin
        processed_path = rf"{crowdin_path}\{version_type}\processed.csv"
        Convert_Lang.process_csv(input_path=rf"{target_path}\process file\{version}_processed.lang",
                                 output_path=processed_path,
                                 special_key=True, debug=conf.debug, version=version)
        trivial.add_bad_translation(template, target_path,
                                    rf"{target_path}\process file",
                                    processed_path, version)
        if crowdin.update_branch(version_type, version, reset=preview_reset):
            Update_Lang.update_info(beta, target_path, 'object', crowdin=True)

        # 等待Preview更新完成后再将Pre-release标记为更新完成

global conf
if __name__ == '__main__':
    run_as_admin()
    conf = config.init_config(r'config/config.json')
    crowdin.init_conf(conf.crowdin_token, conf.crowdin_project_id)

    # main_in = None
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
    # # 提取语言文件位置（git位置）
    # tg_path = r"D:\Documents\GitHub\MCBE-lang"
    # '''
    #     可选择fork https://github.com/Jingji132/MCBE-lang后将仓库下载至本地，将以上路径设置为仓库路径
    # '''
    # csv文件位置（用于上传crowdin）
    # csv_path = r"D:\Users\Economy\git\Gitee\lang-crowdin"

    update_mc_lang(target_path=conf.target_path,  # 提取语言文件至该路径
                   beta=main_beta,  # True:将提取Preview  False:将提取Release
                   crowdin_path=conf.csv_path
                   # mod=True  # 是否修改模板
                   )

    a = input("请按任意键退出~")

# Update_Lang.update_info(True, target_path, [1, 20, 10, 24], 'object')
