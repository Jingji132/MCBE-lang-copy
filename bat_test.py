# python 调用bat文件夹
import subprocess
import os


def bet1():
    # cmd = 'cmd.exe c:\\sam.bat'
    p = subprocess.Popen("cmd.exe /c" + r"D:\Users\Economy\git\Gitee\lang-crowdin\bat_test\1.bat",
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    curline = p.stdout.readline()
    while curline != b'':
        print(curline)
        curline = p.stdout.readline()

    p.wait()
    print(p.returncode)


def bat2():
    os.system(r"D:\Users\Economy\git\Gitee\lang-crowdin\download.bat")


a_dict = {
    'abc': {
        '': 'ABC',
        'hahaha': "HaHaHa"
    }
}
print(a_dict['abc'][''])