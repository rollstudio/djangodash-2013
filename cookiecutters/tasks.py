import os
import shutil
import json
import tempfile
import subprocess

from django.conf import settings
from django.template.defaultfilters import slugify

from celery import task
from cookiecutter.generate import generate_files

from baker import utils


def clone_repo(cookie):
    d = tempfile.mkdtemp()

    os.chdir(d)

    subprocess.call(['git', 'clone', cookie.url, 'tmp'])

    return os.path.join(d, 'tmp')


@task()
def update_repo(cookie):
    # TODO: add commit info to the CookieCutter model
    if not os.path.isdir(cookie.repo_path):
        subprocess.call(['git', 'clone', cookie.url])
    else:
        os.chdir(cookie.repo_path)

        subprocess.call(['git', 'pull'])

    cookie.options = {'repo_name': 'your repo'}
    options_file = os.path.join(cookie.repo_path, 'cookiecutter.json')

    if os.path.isfile(options_file):
        cookie.options.update(json.load(open(options_file)))

    cookie.save()


@task()
def exec_cookiecutter(cookie, options, user_id=None, use_github=True):
    assert 'repo_name' in options
    if user_id is None:
        user_id = 'anon'
        assert use_github is not True

    out = os.path.join(settings.COOKIECUTTERS_TMP, "user_{0}".format(user_id))
    options['repo_name'] = slugify(options['repo_name']).replace('-', '_')

    try:
        if os.path.exists(out):
            shutil.rmtree(out)

        os.makedirs(out)

        repo = clone_repo(cookie)

        generate_files(repo, {'cookiecutter': options}, out)

        repo_path = os.path.join(out, options['repo_name'])
        if use_github:
            repo = utils.create_repository(user_id, options['repo_name'])
            utils.push_directory_to_repo(repo_path, repo)
            return repo.html_url
        else:
            return utils.make_zip(repo_path)
    except:
        pass
