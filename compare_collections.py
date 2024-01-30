# compare_collections.py
import json

def compare_collections():
    try:
        # 读取 Bilibili 收藏的 JSON 文件
        with open('bilibili_collections.json', 'r', encoding='utf-8') as bilibili_file:
            bilibili_collections = json.load(bilibili_file)

        # 读取 Bangumi 收藏的 JSON 文件
        with open('bangumi_collections.json', 'r', encoding='utf-8') as bangumi_file:
            bangumi_collections = json.load(bangumi_file)

        # 获取 Bangumi 中的 subject_id 集合
        bangumi_subject_ids = {entry.get('subject_id') for entry in bangumi_collections if entry.get('subject_id') is not None}

        # 比较 Bilibili 和 Bangumi 的收藏
        output_entries = [{'subject_id': entry.get('subject_id'), 'type': entry.get('type')} for entry in bilibili_collections if entry.get('subject_id') is not None and entry.get('subject_id') not in bangumi_subject_ids]

        # 输出到 JSON 文件
        with open('comparison.json', 'w', encoding='utf-8') as output_file:
            json.dump(output_entries, output_file, ensure_ascii=False, indent=2)

        print("Comparison completed. Output saved to: comparison.json")

    except json.JSONDecodeError:
        print("Error decoding JSON in file.")
    except Exception as e:
        print("An error occurred:", str(e))