import os

import git


def download_repo_git(url, path):
    print('Download start...')
    if not os.path.exists(path):  # 不存在该路径，创建该路径
        os.mkdir(path)
        # 下载git仓库
        git.Repo.clone_from(url, path)
        print('Successfully download, the files are as follows:')
    else:
        # 存在该路径则清空该路径下的所有文件
        for file in os.listdir(path):
            if not file:  # 无旧数据
                # 下载git仓库
                git.Repo.clone_from(url, path)
                print('Successfully download, the files are as follows:')
            else:
                # 如果有旧数据，则拉取git仓库最新更新
                print("Pulling latest update from git repo...")
                git.Repo(path).remotes.origin.pull()
                print('Successfully update, the files are as follows:')

    print(os.listdir(path))


def download_repo(url, path='./download_repo', url_type='git'):
    if url_type == 'git':
        download_repo_git(url, path)
