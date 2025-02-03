from git import Repo

from function import Generate_Template, Produce_Lang, Convert_Lang, trivial
from function.Convert_Lang import process_csv
from function.Generate_Template import read_json
from function.Update_Lang import read_info
from function.base_fun import ver_str
from function.crowdin import update_branch
from function.git_fun import pre_merge, switch
from function.trivial import add_bad_translation


def pre_update(target_path, csv_path):
    ver = read_info(True, tg_path, 'object', pre=True)['ver']
    version = ver_str(ver)
    input(version)

    # 更新模板
    path_=fr"{target_path}\object\template.json"
    template = read_json(path_)
    switch(target_path, 'Pre-Release')
    input(template)

    merged_file = f"{version}_merged.lang"
    Produce_Lang.save(template, target_path, fr"{target_path}/process file/{merged_file}")

    processed_file = f"{version}_processed.lang"
    Produce_Lang.process(fr"{target_path}/process file/{merged_file}",
                         fr"{target_path}/process file/{processed_file}")
    processed_path = rf"{csv_path}\Pre-Release\processed.csv"
    process_csv(input_path=rf"{target_path}\process file\{version}_processed.lang",
                             output_path=processed_path,
                             special_key=True)
    add_bad_translation(template, target_path,
                                rf"{target_path}\process file\{version}_zh_BAD.lang",
                                processed_path)
    input('Sure?')
    update_branch("Pre-Release", version, reset=False)


def pre_test():
    # 测试 pre_merge()
    tg_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    target_branch = "Pre-Release"  # 目标分支名称
    ver = read_info(True, tg_path, 'object', pre=True)['ver']
    # tag= "1.21.60.28"  # 要合并的提交哈希值
    pre_merge(tg_path, target_branch, ver)

if __name__ == "__main__":
    tg_path = r"D:\Users\Economy\git\Gitee\MCBE-lang"
    csv_path = r"D:\Users\Economy\git\Gitee\lang-crowdin"
    pre_update(tg_path, csv_path)

    pass
