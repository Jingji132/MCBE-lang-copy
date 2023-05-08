import Update_Lang
import Produce_Lang
import Generate_Template
import trivial


def update_mc_lang(target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", beta=True, mod=False):
    fd_path, version_in = Update_Lang.find(beta)
    if fd_path is None:
        return
    version = Update_Lang.trans_ver(version_in, beta)
    print("游戏版本：", version, "\n")
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


temp = [
    ["vanilla", 0, 0],
    ["oreui", "Ore UI", 0],
    ["persona", 0, 0],
    ["editor", 0, 0],
    ["experimental_cameras", 0, 0],
    ["chemistry", 0, 0],
    ["custom", 0, "other"]
]

update_mc_lang(target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang",
               beta=True,
               mod=False)
