# Bilibili2Bangumi

这是一个将用户在Bilibili的动画收藏迁移到Bangumi的工具。

它使用Bilibili和Bangumi的API来比较和同步用户的动画收藏。

## 依赖安装

```bash

pip install -r requirements.txt

```

## 使用方法

```bash

python MainScript.py

```

## 代码功能

- Step 1: 使用 `bilibili_anime_scraper` 爬取追番列表
- Step 2: 使用 `bilibili_anime_data_cleaner` 处理追番列表数据
- Step 3: 使用 `MatchAndUpdateIdsDB` 匹配并更新 id
- Step 4: 使用 `bangumi_api_fetch` 获取 Bangumi 收藏
- Step 5: 使用 `compare_collections` 比较 Bilibili 和 Bangumi 的收藏
- Step 6: 使用 `bangumi_api_add_collection` 向 Bangumi 添加收藏

## 特性

- 获取用户 Bilibili 和 Bangumi 的动画收藏。
- 过滤掉 Bangumi 已收藏的条目
- 支持并发请求，提高迁移速度。

## 注意事项

- 在使用脚本之前，请确保已安装相关依赖库。
- 在执行脚本之前，确保已提供正确的参数，包括文件夹路径、MID、ID 和 token 。
