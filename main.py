import Update_Lang
import Produce_Lang


def update_mc_lang(beta=True, target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", template=None):
    fd_path, version_in = Update_Lang.find_lang(beta)
    if fd_path is None:
        return
    version = Update_Lang.transform_version(version_in, beta)
    print(version)
    Update_Lang.copy_lang(fd_path, target_path, "text")
    Update_Lang.update_readme(version, target_path)
    merged_file = f"{version}_merged.lang"
    Produce_Lang.save_lang(template, file_name=merged_file)
    Produce_Lang.process_lang(merged_file, f"{version}_processed.lang", f"{version}_onlykey.lang")


temp = [
    ["vanilla", 0, 0],
    ["oreui", "Ore UI", 0],
    ["persona", 0, 0],
    ["editor", 0, 0],
    ["experimental_cameras", 0, 0],
    ["chemistry", 0, 0],
    ["custom", 0, "other"]
]

update_mc_lang(beta=True,
               target_path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
               template=temp)
