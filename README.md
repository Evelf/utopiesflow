

# Host packages

> sudo apt install python-dev python-setuptools
> sudo apt install libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
> sudo apt install python-psycopg2 postgresql-server-dev-all

Doc for Pillow install: https://pillow.readthedocs.io/en/3.0.0/installation.html#linux-installation

# To dump the database

> pg_dump -Ft dbname > filename

# Setup the database

> createuser -P -S -e utopiesflow
Will ask for a password

> postgres=# CREATE DATABASE utopiesflow OWNER utopiesflow;
> pg_restore -d utopiesflow 20171108-dump-utopiesflow.tar

# Installing

> mkvirtualenv utopiesflow
> (utopiesflow) pip install -r requirements.txt

# Running

> (utopiesflow) ./manage.py runserver
