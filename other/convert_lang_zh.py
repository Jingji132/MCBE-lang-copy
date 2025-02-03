import csv
import os

from function import Produce_Lang
from function.Convert_Lang import processed_to_dict_new, processed_to_dict
from function.base_fun import make_dir


def convert_zh_lang(is_json=False, is_csv=False):
    source_path = r"D:\Users\Economy\git\GitHub\mclangcn\texts"
    process_path = r"D:\Users\Economy\git\Gitee\process_test"
    path4 = os.path.join(process_path, 'processed.lang')
    make_dir(process_path)
    Produce_Lang.process(origin_path=rf"{source_path}\zh_CN.lang", processed_path=path4)

    if is_json:
        convert_path = os.path.join(process_path, 'processed.json')
        with open(convert_path, 'w+', encoding='utf-8') as f:
            json.dump(processed_to_dict(path4), f, ensure_ascii=False) # type: ignore

    if is_csv:
        # input_path = r"D:\Users\Economy\git\Gitee\MCBE-lang\other\1.21.0 release_processed.lang"
        the_dict = processed_to_dict_new(path4)
        # lang_dict = processed_to_dict(path4)
        convert_path = os.path.join(process_path, 'processed.csv')
        headers = ['Key', 'Source string', 'Context', 'Translation']
        rows = []
        for key in the_dict:
            rows.append((key, None, the_dict[key]['crowdinContext'], the_dict[key]['text']))
        with open(convert_path, 'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
