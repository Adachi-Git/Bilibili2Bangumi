import requests
import json
from concurrent.futures import ThreadPoolExecutor

def add_bangumi_collection(entry, access_token):
    subject_id = entry.get('subject_id')
    type = entry.get('type')

    # 构建请求的 URL
    url = f'https://api.bgm.tv/v0/users/-/collections/{subject_id}'

    # 构建请求的 JSON 数据
    data = {
        "type": type,
        "rate": 0,  # 默认不评分，你可以根据需要修改
        "comment": "",
        "private": True,
        "tags": [""]
    }

    # 构建请求头部信息
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Adachi/BangumiMigrate(https://github.com/Adachi-Git/BangumiMigrate)'
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=data)

        # 检查响应状态码
        if response.status_code == 202:
            print(f"Collection added successfully for subject_id {subject_id}.")
        else:
            print(f"Failed to add collection for subject_id {subject_id}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while processing subject_id {subject_id}: {str(e)}")

def bangumi_api_add_collection(access_token):
    try:
        # 读取比较结果的 JSON 文件
        with open('comparison.json', 'r', encoding='utf-8') as comparison_file:
            comparison_entries = json.load(comparison_file)

        # 使用线程池进行并发请求
        with ThreadPoolExecutor() as executor:
            # 提交每个 entry 的处理任务
            futures = [executor.submit(add_bangumi_collection, entry, access_token) for entry in comparison_entries]

            # 等待所有任务完成
            for future in futures:
                future.result()

        print("All collections added successfully.")

    except json.JSONDecodeError:
        print("Error decoding JSON in file.")
    except Exception as e:
        print("An error occurred:", str(e))
