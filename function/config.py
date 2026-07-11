import json
from pathlib import Path
from typing import Any, Dict, Optional
# # 提取语言文件位置（git位置）
# tg_path = r"D:\Documents\GitHub\MCBE-lang"
# '''
#     可选择fork https://github.com/Jingji132/MCBE-lang后将仓库下载至本地，将以上路径设置为仓库路径
# '''
#
# # csv文件位置（用于上传crowdin）
# csv_path = r"D:\Users\Economy\git\Gitee\lang-crowdin"

class Config:
    # 基础配置
    env: str = "dev"
    debug: bool = True

    target_path: Path = Path(r"D:\Documents\GitHub\MCBE-lang")
    csv_path: Path = Path(r"D:\Users\Economy\git\Gitee\lang-crowdin")
    crowdin_token = None
    crowdin_project_id = None

    def load_dict(self, data: Dict[str, Any], **kwargs):
        for k, v in data.items():
            setattr(self, k, v)

def init_config(json_config):
    with open(json_config, "r", encoding="utf-8") as f:
        data = json.load(f)
    the_config = Config()
    the_config.load_dict(data)
    return the_config

if __name__ == '__main__':
    a = init_config(r'../config/config.json')
    print(a.crowdin_project_id)