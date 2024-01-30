import json
import glob
import os
from opencc import OpenCC
import re

def convert_to_simplified_chinese(text):
    cc = OpenCC('t2s')  # t2s 表示繁体到简体
    return cc.convert(text)

def clean_text(text):
    # 清除指定文本内容
    text = re.sub(r'\(仅限港澳台地区\)', '', text)
    text = re.sub(r'\(中配\)', '', text)
    text = re.sub(r'（仅限港澳台地区）', '', text)  # 使用全角括号
    text = re.sub(r'（中配）', '', text)  # 使用全角括号
    text = re.sub(r'（仅限台湾地区）', '', text)  # 使用全角括号
    text = re.sub(r'\(仅限台湾地区\)', '', text)

    return text

def replace_season(text):
    # 替换季度信息
    text = re.sub(r'\(第([一二三四五六七八九十]+)季\)', lambda x: f'第{x.group(1)}季', text)
    text = re.sub(r'\（第([一二三四五六七八九十]+)季\）', lambda x: f'第{x.group(1)}季', text)

    return text


def extract_type(json_folder_path):
    try:
        # 获取当前目录下所有匹配的 JSON 文件路径
        json_files = glob.glob(os.path.join(json_folder_path, 'bilibili_collections.json'))

        if not json_files:
            return []

        # 找到最新的 JSON 文件
        latest_json_file = max(json_files, key=os.path.getctime)

        # 读取 JSON 数据
        with open(latest_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历列表中的每个番剧信息字典
        for item in data:
            follow_status = item.get('follow_status', 0)

            # 根据规则转化为 type 数据
            if follow_status == 2:
                item['type'] = 1
            elif follow_status == 3:
                item['type'] = 2
            elif follow_status == 1:
                item['type'] = 1

            # 删除旧的 follow_status 字段
            item.pop('follow_status', None)

            # 转化为简体中文
            item['name_cn'] = convert_to_simplified_chinese(item['title'])

            # 清除指定文本内容
            item['name_cn'] = clean_text(item['name_cn'])

            # 替换季度信息
            item['name_cn'] = replace_season(item['name_cn'])

            # 删除旧的 title 字段
            item.pop('title', None)

        # 将处理后的数据写回到文件
        with open(latest_json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        # 输出结果
        return 0

    except json.JSONDecodeError:
        return []
    except Exception as e:
        return []