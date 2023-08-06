from .load_config import load_config
import pandas as pd

from .load_setting import load_setting

"""
加载数据集，用于后续处理
"""

def data_access(id:str):
    """
    获取数据集
    :param id: 数据id
    :return: pandas.DataFrame 返回数据集
    """
    SETTING = load_setting()
    config = load_config(id)

    data_file = config["dataset"]["data_files"][0]  # 获取数据集data.csv，默认当前只有一个数据集文件
    data = pd.read_csv(f'{SETTING["base_path"]}/repo_{id}/{data_file["file_name"]}', sep=data_file["sep"])
    return data
