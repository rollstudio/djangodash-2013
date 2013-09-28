import os

from fabric.api import local, lcd

from github3 import login
from gittle import Gittle

from django.conf import settings

from allauth.socialaccount.models import SocialToken


def create_repository(user, repo_name):
    '''Creates a repo with the API and adds our user in order to push the skeleton there'''

    token_model = SocialToken.objects.get(account__user=user, account__provider='github')
    token = token_model.token

    g = login(token=token)

    # TODO: error check
    # happens also when there is already a repo with the same name

    repo = g.create_repo(repo_name)
    repo.add_collaborator(settings.GITHUB_COOKIECUTTER_USERNAME)

    return repo


def push_directory_to_repo(directory, github_repo):
    repo = Gittle.init(directory)

    keypath = settings.GITHUB_PRIVATE_KEY

    message = 'Hello world'

    with lcd(directory):
        local('git init')
        local('git add .')

        local('git commit -m {}', message)

        local('git remote add origin {}'.format(github_repo.clone_url))
        local('git push -u origin master')
