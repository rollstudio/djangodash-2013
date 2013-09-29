import os
import zipfile

from boto.s3.key import Key
from boto.s3.connection import S3Connection

from github3 import login
from gittle import Gittle, GittleAuth

from django.conf import settings

from allauth.socialaccount.models import SocialToken
from cookiecutter.utils import work_in

from django.core.exceptions import ImproperlyConfigured


class FixedGittleAuth(GittleAuth):
    KWARG_KEYS = ()


def create_repository(user_id, repo_name):
    '''
    Creates a repo with the API
    and adds our user in order to push the skeleton there
    '''

    token_model = SocialToken.objects.get(account__user=user_id,
                                          account__provider='github')
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


def make_zip(directory):
    if None in [settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY]:
        raise ImproperlyConfigured('AWS configuration not set.')

    conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(settings.AWS_BUCKET)

    filename = os.path.basename(directory) + '.zip'
    zip_file = zipfile.ZipFile(filename, 'w')

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            arcname = path.replace(directory, '')

            zip_file.write(path, arcname)

    zip_file.close()

    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename(filename)
    k.set_acl('public-read')

    os.remove(filename)

    return k.generate_url(24 * 60 * 60)
