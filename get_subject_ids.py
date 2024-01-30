import json
import sqlite3
import glob
import os

def match_and_update_ids_db(json_folder_path):
    try:
        # 获取当前目录下所有匹配的 JSON 文件路径
        subject_db_path = os.path.join(json_folder_path, 'subject.db')

        if not os.path.exists(subject_db_path):
            print(f"subject.db not found in folder: {json_folder_path}")
            return []

        # 连接 SQLite 数据库
        conn = sqlite3.connect(subject_db_path)
        cursor = conn.cursor()

        # 读取 FollowStatusExtractor 输出的 JSON 文件
        output_filename_all = glob.glob(os.path.join(json_folder_path, 'bilibili_collections.json'))
        if output_filename_all:
            with open(output_filename_all[0], 'r', encoding='utf-8') as json_file:
                titles_data = json.load(json_file)
        else:
            print("No matching JSON file found for titles.")
            return []

        # 匹配并更新 id
        for item in titles_data:
            name_cn = item.get('name_cn', '')

            if name_cn:
                # 使用 name_cn 进行匹配
                cursor.execute("SELECT id FROM bgm_subject WHERE name_cn = ? AND type = ? AND name_cn <> ''", (name_cn, 2))
                match = cursor.fetchone()

                # 如果找到匹配，更新 id
                if match is not None:
                    item['subject_id'] = match[0]

                # 使用 alias 进行匹配
                cursor.execute("SELECT id FROM bgm_subject WHERE alias LIKE ? AND type = ? AND name_cn <> ''", ('%' + name_cn + '%', 2))
                alias_match = cursor.fetchone()

                # 如果找到匹配，更新 id
                if alias_match is not None:
                    item['subject_id'] = alias_match[0]

        print("Debug: Matching and updating IDs completed.")

        # 打印匹配结果
        for idx, item in enumerate(titles_data):
            print(f"Item {idx + 1}: Title: {item.get('name_cn', 'N/A')}, Type: {item.get('type', 'N/A')}, subject_id: {item.get('id')}")

        # 覆盖原有 JSON 文件
        with open(output_filename_all[0], 'w', encoding='utf-8') as json_file:
            json.dump(titles_data, json_file, ensure_ascii=False, indent=2)

        # 关闭数据库连接
        conn.close()

        # 返回匹配结果
        return titles_data

    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {output_filename_all[0]}")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []