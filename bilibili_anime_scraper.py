import requests
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
import logging
import math

log_filename = 'bilibili_scraper.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

def get_bangumi_follow_list_page(user_mid, type_=1, ps=15, pn=1):
    api_url = 'https://api.bilibili.com/x/space/bangumi/follow/list'
    
    params = {
        'vmid': user_mid,
        'type': type_,
        'ps': ps,
        'pn': pn
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.bilibili.com/'
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            logging.error(f"获取数据失败。状态码: {response.status_code}")
    except Exception as e:
        logging.error(f"发生错误: {str(e)}")

def get_bangumi_follow_list(user_mid, type_=1, ps=15):
    logging.info("Starting get_bangumi_follow_list function.")
    try:
        first_page_result = get_bangumi_follow_list_page(user_mid, type_, ps)
        
        if first_page_result['code'] == 0:
            total_count = first_page_result['data']['total']
            total_pages = math.ceil(total_count / ps)

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(get_bangumi_follow_list_page, user_mid, type_, ps, pn) for pn in range(1, total_pages + 1)]
                concurrent_results = [future.result() for future in futures]

            all_titles = []

            for result in concurrent_results:
                if result['code'] == 0:
                    current_page = result['data']['pn']
                    current_page_title_count = len(result['data']['list'])
                    logging.info(f"\n第 {current_page} 页/共 {total_pages} 页 - 当前页标题个数: {current_page_title_count}")
                    for idx, bangumi_detail in enumerate(result['data']['list']):
                        title = bangumi_detail.get('title', 'N/A')
                        follow_status = bangumi_detail.get('follow_status', 'N/A')
                        logging.info(f"标题 {idx + 1}: {title} - Follow Status: {follow_status}")

                        all_titles.append({'title': title, 'follow_status': follow_status})

            # 保存所有标题和 follow_status 到 JSON 文件
            output_filename_all = f"bilibili_collections.json"
            with open(output_filename_all, 'w', encoding='utf-8') as json_file_all:
                json.dump(all_titles, json_file_all, ensure_ascii=False, indent=2)
                
            logging.info(f"总番剧数: {total_count}")
            logging.info(f"实际获取的番剧数: {len(all_titles)}")

        else:
            logging.error(f"错误: {first_page_result['message']}")

    except Exception as e:
        logging.error(f"发生错误: {str(e)}")
    logging.info("Ending get_bangumi_follow_list function.")
