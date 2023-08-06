import json

"""
加载设置文件
"""


def load_setting(path="./static/setting.json"):
    with open(path, 'r', encoding='UTF-8') as f:
        return json.load(f)
