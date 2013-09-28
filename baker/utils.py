import os

from github3 import login
from gittle import Gittle, GittleAuth

from django.conf import settings

from allauth.socialaccount.models import SocialToken
from cookiecutter.utils import work_in


class FixedGittleAuth(GittleAuth):
    KWARG_KEYS = ()


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
    auth = FixedGittleAuth(pkey=open(settings.GITHUB_PRIVATE_KEY))
    repo = Gittle.init(directory, auth=auth)

    files = []
    with work_in(directory):
        for root, dirnames, filenames in os.walk('.'):
            # remove the leading './'
            root = root[2:]
            # skip .git directories
            if '.git' in dirnames:
                dirnames.remove('.git')

            for f in filenames:
                path = os.path.join(root, f)
                files.append(str(path))

    repo.commit(name='bakehouse', message='Hello world', files=files)
    repo.push(github_repo.ssh_url, branch_name='master')
