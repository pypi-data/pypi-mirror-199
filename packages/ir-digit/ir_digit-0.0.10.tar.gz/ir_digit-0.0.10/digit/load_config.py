import json
"""
加载配置文件
"""

def load_config(base_path='./download_repo', config_file='config.json'):
    """
    加载数据对应的config.json配置文件
    :param base_path: 默认数据存放路径 ./download_repo
    :param config_file: 默认配置文件名称 config.json
    :return: dict 返回config.json文件的内容
    """
    with open(f'{base_path}/{config_file}', 'r', encoding='UTF-8') as f:
        return json.load(f)
