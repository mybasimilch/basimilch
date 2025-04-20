# Basimilch web application

On any environment, ensure Python 3 is installed.

## Getting started on UNIX

### Set your environment variables

See the .env.template for details. Reach out to maintainers for secrets.

### Installing requirements

#### Standard approach

- Create a new virtual environment: `python -m venv .venv`
- Activate the virtual environment: `source .venv/bin/activate`
- Install the dependencies: `pip install --upgrade -r requirements-local.txt`
- (To deactivate the virtual environment again): `deactivate`

#### Bleeding edge approach using the [uv package manager for python](https://docs.astral.sh/uv/)

Note: First install uv

- Create a new virtual environment: `uv venv`
- Activate the virtual environment: `source .venv/bin/activate`
- Install the dependencies: `uv pip install -r requirements-local.txt`
- (To deactivate the virtual environment again): `deactivate`

### Setting up the database, admin user and test data

    # Carry out database migrations. This will create a sqlite database
    python manage.py migrate

    # Make sure you have a user with a passowrd to access the application locally
    python manage.py createsuperuser
    python manage.py create_member_for_superusers
    
    # Not required, but usefull
    python manage.py generate_testdata # creates simple test data
    
    # If you want to create more complex test data (not required, but usefull)
    # First install faker: `pip install faker` or `uv pip install faker` if you are using uv.
    python manage.py generate_testdata_advanced

### Run the server

    python manage.py runserver

Navigate to [127.0.0.1:8000](127.0.0.1:8000). You should be able to login with the superuser name or their email address.

## Getting started Windows

Note: This section is likely outdated

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

## Deployment

The application is hosted on Heroku. You'll need:

- Access to the application on heroku. Contact maintainers if you are not.
- The heroku cli.

Afterwards

- To deploy to main branch to basimilch-test: `git push heroku`
- To deploy a feature branch the test application: `git push heroku feature-branch:main`

# Provision basimilch-test with a subset of actual data

## Requirements

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
10. In case you want to drop the test database again, run `sudo -u postgres dropdb $JUNTAGRICO_DATABASE_NAME`
