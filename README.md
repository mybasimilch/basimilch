# Juntagrico Heroku Template for cookiecutter

This template sets up a project to be used with juntagrico.science as hosting.

# Setting up locally to test setup

On any environment install Python 3, and add it to your path

## UNIX

### Set your environment variables

### Installing requirements

    sudo easy_install pip
    sudo pip install virtualenv
    virtualenv --distribute venv
    source ./venv/bin/activate
    pip install --upgrade -r requirements.txt

### Setup DB

    ./manage.py migrate

### Setup Admin User

    ./manage.py createsuperuser
    ./manage.py create_member_for_superusers

### Create Tesdata (not required)

Simple

    ./manage.py generate_testdata

More complex

    ./manage.py generate_testdata_advanced

### Run the server

    ./manage.py runserver

## Windows

### Set your environment variables

This should do it for your local setup:

### Installing requirements

    pip install virtualenv
    virtualenv --distribute venv
    venv\Scripts\activate.bat
    pip install --upgrade -r requirements.txt

### Setup DB

    python -m manage migrate

### Setup Admin User

    python -m manage createsuperuser
    python -m manage create_member_for_superusers

### Create Tesdata (not required)

Simple

    python -m manage generate_testdata

More complex

    python -m manage generate_testdata_advanced

### Run the server

    python -m manage runserver

# Heroku

you have to login to a heroku bash and setup the db and create the admin user as desbribed in the UNIX section

# Provision basimilch-test with a subset of actual data

## Requirements:

- heroku cli
- local postgres database

## How to

1. Export the following environment variables

- $JUNTAGRICO_DATABASE_PASSWORD
- $JUNTAGRICO_DATABASE_USER
- $JUNTAGRICO_DATABASE_NAME

2. Download the latest production backup `heroku pg:backups:download -a basimilch-prod`. The file is called `latest.dump`
3. (If needed): Create a new postgres (super-)user: `sudo -u postgres createuser SUPERUSER PASSWORD $JUNTAGRICO_DATABASE_PASSWORD $JUNTAGRICO_DATABASE_USER`
4. Create a new database: `sudo -u postgres createdb $JUNTAGRICO_DATABASE_NAME`
5. Restore the downloaded backup `pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $JUNTAGRICO_DATABASE_USER -d $JUNTAGRICO_DATABASE_NAME path/to/latest.dump`
6. To delete some of the data to so as to avoid heroku row limit of 10'000 rows, run the following management command `python manage.py prepare_db_for_test`
7. pg_dump --format=c --dbname=postgresql://$JUNTAGRICO_DATABASE_USER:$JUNTAGRICO_DATABASE_PASSWORD@127.0.0.1:5432/$JUNTAGRICO_DATABASE_NAME > ~/path/to/dump
8. Upload the dump to a safe storage, e.g. an AWS S3 bucket and create a presigned url, through the S3 UI
9. Restore the database to basimilch-test: `heroku pg:backups:restore $AWS_PRESIGNED_URL DATABASE_URL --app basimilch-test`. Note: this deletes everything currently in the database
