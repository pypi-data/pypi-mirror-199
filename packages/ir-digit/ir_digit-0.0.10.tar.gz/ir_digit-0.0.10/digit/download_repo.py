import os

import git

from .get_id_or_url import get_url_with_id, get_id_with_url

"""
下载git仓库
"""


def download_repo_git(url, base_path, sec_path):
    print('Download start...')
    if not os.base_path.exists(base_path+sec_path):  # 不存在该路径，创建该路径
        os.mkdir(base_path+sec_path)
        # 下载git仓库
        git.Repo.clone_from(url, base_path+sec_path)
        print('Successfully download, the files are as follows:')
    else:
        # 存在该路径则清空该路径下的所有文件
        for file in os.listdir(base_path+sec_path):
            if not file:  # 无旧数据
                # 下载git仓库
                git.Repo.clone_from(url, base_path+sec_path)
                print('Successfully download, the files are as follows:')
            else:
                # 如果有旧数据，则拉取git仓库最新更新
                print("Pulling latest update from git repo...")
                git.Repo(base_path+sec_path).remotes.origin.pull()
                print('Successfully update, the files are as follows:')
    print(os.listdir(base_path+sec_path))


def download_repo(id_or_url, url_type='git'):
    url = ''
    id = ''

    # 根据输入的id或url判断是id还是url，并获取对应的url和id
    if len(id_or_url) == 6:
        id = id_or_url
        url = get_url_with_id(id)
    else:
        url = id_or_url
        id = get_id_with_url(url)

    base_path = f'./download_repo/'
    sec_path = f'repo_{id}'

    if not os.path.exists(base_path): # 不存在该base_path路径，创建该路径
        os.mkdir(base_path)

    if url_type == 'git':
        download_repo_git(url, base_path, sec_path)
