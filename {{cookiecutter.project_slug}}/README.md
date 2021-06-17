{{cookiecutter.project_name}} API
---------------------------

#### Setup environment

create .env file in root project dir (from env.example):

    cp .env.example .env

#### Create database

from .env file configuration:

    (source .env && eval "echo \"$(cat tools/sql/create_db.sql)\"") | psql

#### Install requirements

    pip install -r requirements.txt
