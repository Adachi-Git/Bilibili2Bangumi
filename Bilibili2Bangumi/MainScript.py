# MainScript.py
from bilibili_anime_scraper import get_bangumi_follow_list
from bilibili_anime_data_cleaner import extract_type
from get_subject_ids import match_and_update_ids_db
from bangumi_api_fetch import get_bangumi_collections
from compare_collections import compare_collections
from bangumi_api_add_collection import bangumi_api_add_collection


def main(json_folder_path, user_mid, user_id, access_token):
    try:
        # Step 1: 使用 bilibili_anime_scraper 爬取追番列表
        get_bangumi_follow_list(user_mid)
        check_step_completion('Step 1')

        # Step 2: 使用 bilibili_anime_data_cleaner 处理追番列表数据
        extract_type(json_folder_path)
        check_step_completion('Step 2')

        # Step 3: 使用 MatchAndUpdateIdsDB 匹配并更新 id
        match_and_update_ids_db(json_folder_path)
        check_step_completion('Step 3')

        # Step 4: 使用 bangumi_api_fetch 获取 Bangumi 收藏
        get_bangumi_collections(user_id, access_token)
        check_step_completion('Step 4')

        # Step 5: 使用 compare_collections 比较 Bilibili 和 Bangumi 的收藏
        compare_collections()
        check_step_completion('Step 5')

        # Step 6: 使用 bangumi_api_add_collection 向 Bangumi 添加收藏
        bangumi_api_add_collection(access_token=access_token)
        check_step_completion('Step 6')

        print("All steps completed successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def check_step_completion(step_name):
    print(f"Step {step_name} completed successfully.")

json_folder_path = r"C:\Users\Darling\Desktop\bangumi"
user_mid = 123456
user_id = 233333
access_token = '4fakcNbEAXV3P43OKDFUfGKeFuSm7tcK8wBRxAjd'

main(json_folder_path, user_mid, user_id, access_token)