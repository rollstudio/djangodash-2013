sudo apt-get update
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

sudo -u postgres createdb bakehouse 2>/dev/null

cd /vagrant

sudo pip install -r requirements/base.txt

export DJANGO_SETTINGS_MODULE=bakehouse.settings.vagrant

python manage.py syncdb --noinput
python manage.py migrate