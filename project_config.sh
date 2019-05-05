apt-get -qqy update
DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
sudo pip install --upgrade pip
sudo pip install werkzeug==0.8.3
sudo pip install flask packaging oauth2client redis passlib flask-httpauth
sudo pip install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests httplib2
sudo pip install Flask-Login==0.1.3
sudo pip install --upgrade google-api-python-client
