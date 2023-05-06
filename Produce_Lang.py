import os


def read(sub_folder="vanilla",
         display=0,
         folder=0,
         path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
         pack_name="Minecraft译名修正"):
    if folder == 0:
        folder = "text"
    lang_path = os.path.join(path, folder, sub_folder, "en_US.lang")
    with open(lang_path, "r", encoding='utf-8') as f:
        line = f.readlines()
        f.close()
    if sub_folder == "vanilla":
        line[1] = f"## {pack_name}\n"  # Minecraft译名修正
    else:
        if display == 0:
            display = sub_folder.replace("_", " ").title()
        line.insert(0, f"\n## {display} strings\n")
    line.append("\n")
    return line


def save(template=None,
         path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", path_append=None,
         file_name="test.lang"):
    if path_append is not None:
        path = os.path.join(path, path_append)
    if template is None:
        template = [["vanilla", 0, 0]]
    file_path = os.path.join(path, file_name)
    with open(file_path, "w", encoding='utf-8') as f:
        for i in template:
            lang_line = read(sub_folder=i[0], display=i[1], folder=i[2],
                             path=path)
            f.writelines(lang_line)
        f.close()


def process(origin, processed="processed.lang",
            onlykey="onlykey.lang",
            path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test", path_append=None):
    if path_append is not None:
        path = os.path.join(path, path_append)
    origin_path = os.path.join(path, origin)
    process_path = os.path.join(path, processed)
    onlykey_path = os.path.join(path, onlykey)
    processed_line = []
    onlykey_line = []
    with open(origin_path, "r", encoding='utf-8') as f:
        line = f.readlines()
        f.close()
    for i in line:
        processed_line.append(i.replace("=", "\t", 1))
        if "=" in i:
            onlykey_line.append(i.split("=")[0] + "\n")
        else:
            onlykey_line.append(i)
    with open(process_path, "w", encoding='utf-8') as f:
        f.writelines(processed_line)
        f.close()
    with open(onlykey_path, "w", encoding='utf-8') as f:
        f.writelines(onlykey_line)
        f.close()

# save_lang(temp, path_append="text", file_name="test_origin.lang")
# process_lang("test_origin.lang", path_append="text")
