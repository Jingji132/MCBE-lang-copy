import os


def update_custom_tips(path=r"D:\Users\Economy\Documents\Gitee\MCBE-lang_UPD_test",
                       read_path=r"text\vanilla\en_US.lang",
                       mod_path=r"other\custom\en_US.lang"):
    read_path = os.path.join(path, read_path)
    mod_path = os.path.join(path, mod_path)
    if not (os.path.isfile(read_path) and os.path.isfile(mod_path)):
        print("路径错误！")
        return
    tips = "tips.game."
    with open(mod_path, 'r', encoding='utf-8') as f:
        origin_lines = f.readlines()
        f.close()
    with open(read_path, 'r', encoding='utf-8') as f:
        read_lines = f.readlines()
        f.close()
    num1 = 0
    for line in origin_lines:
        if tips in line:
            num1 = int(line.split("=")[0].replace(tips, ""))
            # print(num1)
            break
    if num1 == 0:
        print("文件不包含tips！")
        return
    num2 = 0
    for line in read_lines:
        if tips in line:
            num2 += 1
    # print(num2)
    if num2 == num1 - 1:
        print("tips序号无需更新\n")
        return
    print("tips序号待更新")
    num = num2 + 1
    mod_lines = []
    # print(tips_num)
    for line in origin_lines:
        tips_num = tips + str(num)
        tips_num1 = tips + str(num1)
        line = line.replace(tips_num1, tips_num)
        # print(line)
        mod_lines.append(line)
        num += 1
        num1 += 1

    with open(mod_path, 'w', encoding='utf-8') as f:
        f.writelines(mod_lines)
        print("更新完成\n")
        f.close()


# update_custom_tips()
