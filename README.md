djangodash-2013
===============


    $ virtualenv env
    $ . env/bin/activate
    $ git clone repo dash13

    $ sudo apt-get install postgres libpq-dev
    $ sudo -u postgres psql
    > CREATE DATABASE dash;
    > CREATE ROLE user LOGIN;
    # where `user` is the user that will execute uwsgi
    > \q
    # check that you can login with your user
    $ psql -d dash

    $ sudo apt-get install rabbitmq-server

    $ cd dash13
    $ mkdir logs
    $ pip install -r requirements/production.txt

    $ sudo -s
    # export DJANGO_SETTINGS_MODULE=bakehouse.settings.production
    #  export SECRET_KEY='random key'
    #  export AWS_ACCESS_KEY_ID=
    #  export AWS_SECRET_ACCESS_KEY
    # ./manage.py migrate
    
Edit bakehouse.settings.production
change `ALLOWED_HOSTS`, `AWS_STORAGE_BUCKET_NAME` and `STATIC_URL`.

Then you can start uwsgi. Remember to drop root privileges using the `uid` and `gid` flags:

    # uwsgi --ini uwsgi.ini --uid 1000 --gid 1003

Now you have to start a celery worker:
    $ ./manage.py celery worker --loglevel=info
