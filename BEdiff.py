import os


def extract(path_read, extract_list):
    with open(path_read, 'r', encoding='utf-8') as f:
        line = f.readlines()
    # line2 = []
    dict2 = {}
    for l in line:
        l2 = l.replace('=', '\t')
        l3 = l2.split('\t')
        tag = l3[0].split('.')[0]
        if tag in extract_list:
            # line2.append(l2)
            dict2[l3[0]] = l3[1]
    return dict2
    # with open(path_write, 'w', encoding='utf-8') as f:
    #     f.writelines(line2)


def wiki_find(path_read):
    with open(path_read, 'r', encoding='utf-8') as f:
        line = f.readlines()
    new_list = []
    new_dict = {}
    for l in line:
        if 'Sprite' in l:
            # print(l)
            new_list.append(l)
            l2 = l.split(' || ')
            new_dict[l2[1]] = [l2[2], l2[3].replace('[', '').replace(']', '').replace(' ||\n', '')]
    # for i in new_dict:
    #     print(i, new_dict[i])
    return new_dict


def BE_compare(path_read, wiki_dict):
    with open(path_read, 'r', encoding='utf-8') as f:
        line = f.readlines()
    BE_dict = {}
    for l in line:
        if 'Sprite' in l:
            l2 = l.split('\t')
            BE_dict[l2[1]] = [l2[2], l2[3].replace('\n', '')]
    for i in BE_dict:
        print(i, BE_dict[i])


dict1 = wiki_find(r"D:\Users\Economy\Documents\Gitee\mclangdiff\wiki1.txt")
dict2 = wiki_find(r"D:\Users\Economy\Documents\Gitee\mclangdiff\zh_DF.txt")
all_same = {}
not_same = {}
not_exist = {}
for i in dict2:
    if i in dict1:
        if dict1[i] == dict2[i]:
            all_same[i] = dict1[i]
        else:
            not_same[i] = [dict1[i], dict2[i]]
    else:
        not_exist[i] = dict2[i]
print('\nall same:')
for i in all_same:
    print(i, all_same[i])
print('\nnot same:')
for i in not_same:
    print(i, not_same[i])
print('\nnot exist:')
for i in not_exist:
    print(i, not_exist[i])

# BE_compare(r"D:\Users\Economy\Documents\Gitee\mclangdiff\zh_DF.txt", dict1)


def BE_diff():
    EN_path = r"D:\Users\Economy\git\Gitee\MCBE-lang\text\vanilla\en_US.lang"
    BE_path = r"D:\Users\Economy\git\Gitee\MCBE-lang\text\vanilla\zh_CN.lang"
    BE_write = r"D:\Users\Economy\Documents\Gitee\mclangdiff\zh_BE.txt"
    FX_path = r"D:\Users\Economy\git\GitHub\mclangcn\texts\zh_CN.lang"
    FX_write = r"D:\Users\Economy\Documents\Gitee\mclangdiff\zh_FX.txt"
    DF_write = r"D:\Users\Economy\Documents\Gitee\mclangdiff\zh_DF.txt"

    ex_list = ['effect', 'enchantment', 'entity', 'feature', 'item', 'itemGroup', 'potion', 'tile', 'tipped_arrow', ]

    EN_dict = extract(EN_path, ex_list)
    BE_dict = extract(BE_path, ex_list)
    FX_dict = extract(FX_path, ex_list)
    line_final = []
    for i in BE_dict:
        if BE_dict[i].replace(' ', '') != FX_dict[i].replace(' ', ''):
            en = EN_dict[i].replace('\n', '')
            line_final.append(
                f"|_BIG_KUO__BIG_KUO_Sprite|{en}_BIG_HUI__BIG_HUI_ || {en} || {BE_dict[i]} || [[{FX_dict[i]}]] ||\n|-\n".replace(
                    '_BIG_KUO_', '{').replace('_BIG_HUI_', '}'))
    with open(DF_write, 'w', encoding='utf-8') as f:
        f.writelines(line_final)
