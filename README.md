# MCBE-lang-copy

* 查找并复制本机内Minecraft BE（Windows）中英语言文件（.lang）到新的文件夹 [Update_Lang.py](Update_Lang.py)
* 自定义生成包含多个包的语言文件模板 [Generate_Template.py](Generate_Template.py)
* 根据模板与找到的.lang文件生成合成所需的语言文件 [Produce_Lang.py](Produce_Lang.py)
* ~~更新自定义tips序号 [trivial.py](trivial.py)（游戏已将tips键名拆分，基本用不到了）~~
* lang ⇋ json/csv [Convert_Lang.py](Convert_Lang.py)（用于crowdin上传与下载）
* 生成Java版最新中英语言文件（csv），需要本地安装最新版游戏 [JE_lang.py](JE_lang.py)（用于导入crowdin翻译记忆）
* git切换分支与提交 [git_fun.py](git_fun.py)（获取版本间的diff文件，在main.py中作为判断版本是否为预发布版的条件，仓库格式为[Jingji132/MCBE-lang](https://github.com/Jingji132/MCBE-lang)</small>）
* crowdin上传 [crowdin.py](crowdin.py)（需要创建config.json文件）（使用[crowdin-api-client-python](https://github.com/crowdin/crowdin-api-client-python) 1.15.2）
