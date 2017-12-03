## Install

### Virtualenv with python3:
mkvirtualenv -p python3 ithikithi-be

### Install requirements:
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

## Run

### Run project
python manage.py runserver
