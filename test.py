zh_BE = r"D:\Users\Economy\git\Gitee\MCBE-lang\text\vanilla\zh_CN.lang"
en_BE = r"D:\Users\Economy\git\Gitee\MCBE-lang\text\vanilla\en_US.lang"

zh_fix = r"D:\Users\Economy\git\GitHub\mclangcn\texts\zh_CN.lang"


def open_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lang_dict = {}
    for line in lines:
        line = line.split('#', 1)[0]
        if '=' in line:
            line = line.split('=', 1)
            lang_dict[line[0]] = line[1].replace('\t', '')
    # print(lang_dict)
    return lang_dict


if __name__ == '__main__':
    zh_lang = open_file(zh_BE)
    en_lang = open_file(en_BE)
    mclangcn = open_file(zh_fix)
    line2 = []
    for key in zh_lang:
        key1 = key.split('.', 1)[0]
        if key1 in ['item', 'tile', 'itemGroup', 'effect', 'enchantment', 'entity', 'feature']:
            if key not in mclangcn:
                continue
            if zh_lang[key] == mclangcn[key]:
                continue
            if zh_lang[key].replace(' ', '') == mclangcn[key]:
                continue
            line2.append(key+'\n'+en_lang[key].replace('\n', '')+'\t'+zh_lang[key]+'\t'+mclangcn[key]+'\n')

    with open('Badrock_diff.txt', 'w+', encoding='utf-8') as f:
        f.writelines(line2)
    pass
