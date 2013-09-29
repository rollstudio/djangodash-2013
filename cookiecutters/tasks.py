import os
import shutil
import json

from gittle import Gittle

from django.conf import settings

from cookiecutter.generate import generate_files

from baker import utils

from celery import task
from celery import current_task


@task()
def update_repo(cookie):
    # TODO: add commit info to the CookieCutter model
    if not os.path.isdir(cookie.repo_path):
        repo = Gittle.clone(cookie.url, cookie.repo_path)
    else:
        repo = Gittle(cookie.repo_path, cookie.url)
        repo.pull()

    cookie.options = {'repo_name': 'your repo'}

    options_file = os.path.join(cookie.repo_path, 'cookiecutter.json')
    if os.path.isfile(options_file):
        cookie.options.update(json.load(open(options_file)))

    cookie.save()


@task()
def exec_cookiecutter(cookie, options, user_id=None, use_github=True):
    # TODO: not fully implemented
    assert 'repo_name' in options
    if user_id is None:
        user_id = 'anon'
        assert use_github is not True

    out = os.path.join(settings.COOKIECUTTERS_TMP, "user_{0}".format(user_id))

    try:
        os.makedirs(out)

        print out

        generate_files(cookie.repo_path, {'cookiecutter': options}, out)

        if use_github:
            repo = utils.create_repository(user_id, options['repo_name'])

            utils.push_directory_to_repo(os.path.join(out, options['repo_name']), repo)
        else:
            # make zippone
            pass
    finally:
        if os.path.exists(out):
            shutil.rmtree(out)
