import Update_Lang
import Produce_Lang
import Generate_Template
import Process_json
import trivial


def update_mc_lang(target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", beta=True, mod=False):
    fd_path, version_in = Update_Lang.find(beta)
    if fd_path is None:
        return
    version, ver = Update_Lang.trans_ver(version_in, beta)
    print("游戏版本：", version, "\n")
    ver_old = Update_Lang.read_info(beta, target_path, 'object')
    print(ver_old)
    compare, major = Update_Lang.compare_ver(ver, ver_old)
    if compare:
        Update_Lang.update_info(beta, target_path, ver, 'object')
    if major:
        Update_Lang.update_info(beta, target_path, ver_old, 'object', pre=True)
    Update_Lang.copy(fd_path, target_path, "text")
    Update_Lang.readme(version, target_path)
    trivial.update_custom_tips(target_path)
    merged_file = f"{version}_merged.lang"
    template = Generate_Template.update(target_path, path_append_list=["other"])
    Produce_Lang.save(template, path=target_path, path_append="other", file_name=merged_file)
    if mod:
        Generate_Template.modify(target_path)
    Produce_Lang.process(merged_file, f"{version}_processed.lang", f"{version}_onlykey.lang",
                         path=target_path, path_append="other")
    Process_json.process_en_json(f"{version}_processed.lang", path=target_path, path_append="other",
                                 json_path=r"D:\Users\Economy\git\Gitee\lang-crowdin\processed.json")


update_mc_lang(target_path=r"D:\Users\Economy\git\Gitee\MCBE-lang",  # 提取语言文件至该路径
               beta=True,  # True:将提取Preview  False:将提取Release
               mod=True  # 是否修改模板
               )
