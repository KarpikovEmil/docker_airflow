import pandas as pd
import json

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

json_str = """[ { "id": 2266101084, "color": 48, "name": "Inbox", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "inbox_project": true, "url": "https://todoist.com/showProject?id=2266101084" }, { "id": 2266102370, "order": 1, "color": 31, "name": "Работа", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2266102370" }, { "id": 2281199547, "order": 2, "color": 46, "name": "Проекты", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2281199547" }, { "id": 2276172551, "order": 3, "color": 41, "name": "Финансы", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2276172551" }, { "id": 2275765087, "order": 4, "color": 33, "name": "Организационно-бытовые задачи", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275765087" }, { "id": 2275777802, "order": 5, "color": 36, "name": "Красота и здоровье", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275777802" }, { "id": 2275765259, "order": 6, "color": 37, "name": "Личная эффективность", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2275765259" }, { "id": 2286290517, "order": 7, "color": 34, "name": "Soft", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2286290517" }, { "id": 2276173208, "order": 8, "color": 30, "name": "Семья", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2276173208" }, { "id": 2281200101, "order": 9, "color": 35, "name": "Друзья", "comment_count": 0, "shared": false, "favorite": false, "sync_id": 0, "url": "https://todoist.com/showProject?id=2281200101" } ]"""
tasks = """[{
    "assignee": 2671142,
    "assigner": 2671362,
    "comment_count": 10,
    "completed": true,
    "content": "Buy Milk",
    "description": "",
    "due": {
        "date": "2016-09-01",
        "datetime": "2016-09-01T09:00:00Z",
        "recurring": false,
        "string": "tomorrow at 12",
        "timezone": "Europe/Moscow"
    },
    "id": 2995104339,
    "label_ids": [
        2156154810,
        2156154820,
        2156154826
    ],
    "order": 1,
    "priority": 1,
    "project_id": 2203306141,
    "section_id": 7025,
    "parent_id": 2995104589,
    "url": "https://todoist.com/showTask?id=2995104339"
},{"end" : true}]"""

def json_to_df(data):
    json_object = json.loads(data)
    df = pd.json_normalize(json_object)
    return df


json_to_df(tasks)