import requests


def get_url_with_id(url_param):
    """
    通过url获取id,使用华为云服务器
    :param url_param:文档下载连接
    :return:id:str
    """
    # url = "http://127.0.0.1:8000/url_to_id/" # 本地测试url
    url = "http://124.70.200.79:9562/url_to_id/" # 线上运行url
    body = {"url": url_param}
    response = requests.post(url, json=body)
    data = response.json()
    if data['status'] == 'normal':
        return data['id']
    else:
        return "函数get_url_with_id出现错误，请检查输入的url_param是否正确"

def get_id_with_url(id):
    """
    通过id获取url,使用华为云服务器
    :param id: 数据id
    :return: url:str
    """
    url = "http://127.0.0.1:8000/id_to_url" # 本地测试url
    # url = "http://124.70.200.79:9562/id_to_url" # 线上运行url
    response = requests.get(url + "/" + id)
    data = response.json()
    if data['status'] == 'normal':
        return data['url']
    else:
        return "函数get_id_with_url出现错误，请检查输入的id是否正确"


