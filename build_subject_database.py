import os
import jsonlines
import sqlite3
import json
import re
import html

def extract_aliases_from_infobox(infobox):
    try:
        match = re.search(r'\|别名=([\s\S]*?)\}', infobox)
        if match:
            aliases_section = match.group(1).strip()
            if aliases_section:
                aliases = re.findall(r'\[([\s\S]*?)\]', aliases_section)
                alias_list = [html.unescape(alias.strip()).encode('utf-8').decode('utf-8') for alias in aliases if alias.strip()]
                return json.dumps(alias_list, ensure_ascii=False)
        return "[]"
    except json.JSONDecodeError:
        return "[]"

def create_database_table():
    conn = sqlite3.connect('subject.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bgm_subject (
            id INTEGER PRIMARY KEY,
            name TEXT,
            name_cn TEXT,
            alias TEXT,
            type INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data_to_db(file_path):
    if os.path.exists('subject.db'):
        os.remove('subject.db')

    conn = sqlite3.connect('subject.db', timeout=10)
    cursor = conn.cursor()
    create_database_table()

    with jsonlines.open(file_path) as reader:
        for line in reader:
            if line.get('type') == 2:
                values = (
                    line.get('id', None),
                    line.get('name', None),
                    line.get('name_cn', None),
                    extract_aliases_from_infobox(line.get('infobox', '')),
                    line.get('type', None)
                )
                insert_statement = '''
                    INSERT INTO bgm_subject (id, name, name_cn, alias, type)
                    VALUES (?, ?, ?, ?, ?)
                '''
                cursor.execute(insert_statement, values)

    conn.commit()
    conn.close()

# 插入数据到数据库（只提取 type 为 2 的数据，删除原有数据库文件，然后新建数据库）
insert_data_to_db('subject.jsonlines')