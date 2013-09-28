import os
import shutil

from django.conf import settings
from gittle import Gittle
from celery import task
# from cookiecutter.generate import generate_files
from baker import utils


@task()
def update_repo(cookie):
    # TODO: add commit info to the CookieCutter model
    if not os.path.isdir(cookie.repo_path):
        repo = Gittle.clone(cookie.url, cookie.repo_path)
    else:
        repo = Gittle.init(cookie.repo_path)
        repo.pull()

    cookie.options = {'repo_name': 'your repo'}

    options_file = os.path.join(cookie.repo_path, 'cookiecutter.json')
    if os.path.isfile(options_file):
        cookie.options.update(json.load(open(options_file)))

    cookie.save()


@task()
def exec_cookiecutter(cookie, user, options):
    assert 'repo_name' in options

    out = os.path.join(settings.COOKIECUTTERS_TMP, user.username)
    try:
        generate_files(cookie.repo_path, {'cookiecutter': options}, out)
        repo = utils.create_repository(user, options['repo_name'])
        utils.push_directory_to_repo(os.path.join(out, options['repo_name']), repo)
    finally:
        shutil.rmtree(out)
