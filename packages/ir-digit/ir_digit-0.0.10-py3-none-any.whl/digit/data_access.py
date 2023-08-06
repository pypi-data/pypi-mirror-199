from .load_config import load_config
import pandas as pd

"""
加载数据集，用于后续处理
"""

def data_access(base_path='./download_repo'):
    """
    获取数据集
    :param base_path: 数据存放路径
    :return: pandas.DataFrame 返回数据集
    """
    config = load_config(base_path)

    data_file = config["dataset"]["data_files"][0]  # 获取数据集data.csv，默认当前只有一个数据集文件
    data = pd.read_csv(f'{base_path}/{data_file["file_name"]}', sep=data_file["sep"])
    return data
