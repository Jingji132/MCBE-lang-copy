import crowdin_api
import json


# 读取配置文件
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
token = config_data["token"]
project_id = 590029
file_id = 11
file_name = r"D:\Users\Economy\git\Gitee\lang-crowdin\Preview\processed.json"
client = crowdin_api.CrowdinClient(token=token)


def init(version_type='Preview'):
    global file_name, file_id
    if version_type == 'Preview':
        file_id = 11
    elif version_type == 'Release':
        file_id = 41
    elif version_type == 'Pre-Release':
        file_id = 45
    else:
        print("版本类型有误！")
        return
    file_name = fr"D:\Users\Economy\git\Gitee\lang-crowdin\{version_type}\processed.json"


def update():
    # 11/41/45 : Preview/Release/Pre-Release
    storage = client.storages.add_storage(open(file_name, 'rb'))
    print(file_id, file_name)
    my_file = client.source_files.update_file(project_id, file_id, storage['data']['id'])
    print(my_file)


def find_info():
    try:
        project_branches = client.source_files.list_project_branches(projectId=project_id)

        for i in project_branches['data']:
            print(i['data'])
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def file():
    try:
        project_files = client.source_files.list_files(projectId=project_id)

        for f in project_files['data']:
            print(f)
            if f['data']['name'] == 'processed.json':  # 替换成您的 JSON 文件名
                file_id = f['data']['id']
                print(f"File ID: {file_id}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


# find_info()
# file()
