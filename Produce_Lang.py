import os

import Generate_Template
import base_fun


def save(template=None,
         read_dir_path=r"...\MCBE-lang",
         save_path=r"...\MCBE-lang\other\test.lang",
         zh=False):
    def read(folder='text',
             sub_folder="vanilla",
             display='',
             path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
             pack_name="Minecraft译名修正",
             is_zh=False):
        if is_zh:
            lang_type = 'zh_CN.lang'
            lang_path = os.path.join(path, folder, sub_folder, lang_type)
        else:
            lang_type = 'en_US.lang'
            lang_path = os.path.join(path, folder, sub_folder, lang_type)

        # print(lang_path)
        if not os.path.exists(lang_path):
            print("未找到当前模板中的", folder, "/", sub_folder, lang_type, "，已跳过相关操作")
            return False
        with open(lang_path, "r", encoding='utf-8') as f:
            line = f.readlines()
            f.close()
        if sub_folder == "vanilla":
            line[1] = f"## {pack_name}\n"  # Minecraft译名修正
        else:
            if display == '':
                display = sub_folder.replace("_", " ").title()
            line.insert(0, f"\n## {display} strings\n")
        line.append("\n")
        return line

    if template is None:
        template = Generate_Template.old_to_new([[["vanilla", 0, 0]]])

    base_fun.make_dir_path(save_path)
    with open(save_path, "w", encoding='utf-8') as f:
        for _i in template:
            for _ii in template[_i]:
                context = template[_i][_ii]
                lang_line = read(folder=_i, sub_folder=_ii, display=context['display'],
                                 path=read_dir_path, is_zh=zh)
                if lang_line:
                    f.writelines(lang_line)


def process(origin_path, processed_path):
    with open(origin_path, "r", encoding='utf-8') as f:
        line = f.readlines()

    processed_line = []
    for i in line:
        if "=" in i:
            i = base_fun.replace_rule(i)
            processed_line.append(i)
        else:
            i = i.replace("\t", " ")
            processed_line.append(i)

    with open(processed_path, "w", encoding='utf-8') as f:
        f.writelines(processed_line)


# save_lang(temp, path_append="text", file_name="test_origin.lang")
# process_lang("test_origin.lang", path_append="text")

if __name__ == '__main__':
    save(None,
         r"D:\Users\Economy\git\Gitee\MCBE-lang",
         r"D:\Users\Economy\git\Gitee\MCBE-lang\test\test_zh.lang",
         zh=True)
