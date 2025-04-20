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

Note: This is not required if you [use a local copy of production data](#how-to-run-basimilch-locally-with-a-copy-of-the-production-data)

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

## How to run basimilch locally with a copy of the production data

...and upload production data to basimilch test for testing

### Requirements

- heroku cli
- postgres database running in docker

### Use production data locally

0. Create a new backup: `heroku pg:backups:capture --app basimilch-prod`

1. Download the production backup `heroku pg:backups:download -a basimilch-prod`. The file is called `latest.dump`

2. Export the following environment variables
    - $JUNTAGRICO_DATABASE_PASSWORD
    - $JUNTAGRICO_DATABASE_USER
    - $JUNTAGRICO_DATABASE_NAME
    - $DB_DUMP_STORAGE_LOCATION
Note: If you already have an .env file, you can export them like so on ubuntu:  `set -a && source .env && set +a`

3. Move the file to the storage location
`mv latest.dump $DB_DUMP_STORAGE_LOCATION/$JUNTAGRICO_DATABASE_NAME.dump`

4. Run your postgres database inside your docker conatiner, and mount your db storage location inside the running container.
`docker run --rm -v $DB_DUMP_STORAGE_LOCATION:/home/postgres/dump -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=$JUNTAGRICO_DATABASE_PASSWORD postgres:14`

5. Create a new database inside the docker container: `docker exec -u postgres postgres createdb $JUNTAGRICO_DATABASE_NAME`
6. Restore the downloaded backup `docker exec -u postgres postgres pg_restore --verbose --clean --no-acl --no-owner -h localhost -d $JUNTAGRICO_DATABASE_NAME /home/postgres/dump/$JUNTAGRICO_DATABASE_NAME.dump`
7. (If you are running a higher juntagrico version locally than in production) `python manage.py migrate`
8. (Optional) To stop the docker container and delete the database, run `docker stop postgres`

### Upload the production data to basimilch test for testing

After an update has been made, it might be useful for testers to test with the current production data. Follow steps 1-5 above. Then:

0. (No longer required. See prepare_db_for_test.py) To delete some of the data avoid heroku row limit of 10'000 rows (free tier), run the management command `python manage.py prepare_db_for_test`
1. `docker exec postgres pg_dump --format=c --dbname=postgresql://$JUNTAGRICO_DATABASE_USER:$JUNTAGRICO_DATABASE_PASSWORD@127.0.0.1:5432/$JUNTAGRICO_DATABASE_NAME > $DB_DUMP_STORAGE_LOCATION/$JUNTAGRICO_DATABASE_NAME.sql`
2. Upload the dump to a safe storage, e.g. an AWS S3 bucket and create a presigned url, through the S3 UI
3. Export the presigned url `export AWS_PRESIGNED_URL= url obtained from step 3`
4. Restore the database to basimilch-test: `heroku pg:backups:restore $AWS_PRESIGNED_URL DATABASE_URL --app basimilch-test`. Note: this deletes everything currently in the database
