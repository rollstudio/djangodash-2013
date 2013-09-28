import os

from gittle import Gittle
from celery import task


@task()
def update_repo(cookie):
    if not os.path.isdir(cookie.repo_path):
        repo = Gittle.clone(cookie.url, cookie.repo_path)
    else:
        repo = Gittle.init(cookie.repo_path)
        repo.pull()

    options_file = os.path.join(cookie.repo_path, 'cookiecutter.json')
    if os.path.isfile(options_file):
        cookie.options = open(options_file).read()
        cookie.save()
