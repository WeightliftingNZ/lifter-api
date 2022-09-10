# Lifter API Documentation

Did you mean [Lifter API Wrapper Documentation](https://weightliftingnz.github.io/lifter-api-wrapper)?

## Hosting

This is hosted on [Digital Ocean's App Platform](https://www.digitalocean.com/products/app-platform). Code changes to this repository on the main branch will automatically trigger changes to the live web application.

The backend API and the frontend are set up on their own apps. And there is set up required (see below). Normally, this is first time.

### Setting up the Backend

#### 1. Run command

This is the run command:

```shell

gunicorn --worker-tmp-dir /dev/shm config.wsgi

```

Note the `config.wsgi`

#### 2. API Domain

Ensure the domain provided this is set to: `https://api.lifter.shivan.xyz`.

This may take time to configure. And this is all handled by Digital Ocean.

#### 3. Backend Environment Variables

The following environment variables should be set:

```shell
DJANGO_DEVELOPMENT = 0
ALLOWED_HOSTS = ${APP_DOMAIN}
DATABASE_URL = ${db.DATABASE_URL}
CORS_ALLOWED_ORIGINS = https://lifter.shivan.xyz
SECRET_KEY = <see below>
HASHID_FIELD_SALT = <see below>
SENTRY_DSN_1 = <see below>
SENTRY_DSN_2 = <see below>
SENTRY_SAMPLE_RATE = 1.0 # depends
```

##### Secret Keys

Running the below code will provide the a random hash to set `SECRET_KEY` and `HASHID_FIELD_SALT`.

```shell

$ make generate-key

ffqd6(a-&dqk#znv!4@!1u=&_et9b^wdgpm5cz4=^b=9_3xaux

```

Tip: Use `make generate-key | pbcopy` on MacOS if you want to copy the key to clipboard.

##### Sentry Environment Variables

These are mapped accordingly:

```python
sentry_sdk.init(
    dsn=f"https://{SENTRY_DSN_1}.ingest.sentry.io/{SENTRY_DSN_2}",
    integrations=[
        DjangoIntegration(),
    ],
    # set this to between 0 and 1.0 when in production
    trace_sample_rate=SENTRY_SAMPLE_RATE
```

#### 4. Migrations and Superuser

In the console of the Digital Ocean App Platform migrations and a creation of a superuser is required.

Migration:

```shell
python manage.py makemigrations
python manage.py migrate
```

Create superuser:

```shell
python manage.py createsuperuser
```

#### 5. Debugging

There is a `debug.log` file provided.

Use this command to follow the debug log in realtime:

```shell
tail -f debug.log
```

### Setting up the Frontend

#### 1. Catch-all

Catch-all needs to be set to `index.html`. This is because `react-router` uses the url link to decide what content to serve, rather than a url requesting something on the server. That means a url other than the root url will return a 404 error.

A catch-all will return the root url for processing by javascript.

#### 2. Main Domain

Another domain is provided. Ensure this is set to: `https://lifter.shivan.xyz`.

This takes time and is all handled by Digital Ocean.

#### 3. Frontend Environment Variables

The environment variables need to be set:

```shell
REACT_APP_API_URL = "https://api.lifter.shivan.xyz/v1"
```

## Local Development

Base requirements include:

- Docker v20.10.8
- Docker Compose v2.0.0
- Node v16.14.2
- Python v3.10.0

Here is the rough layout of the application:

```shell
lifter-api
├── backend/
│   ├── ... Django Rest Framework stuff
├── frontend
│   ├── ... React Typescript TailwindCSS stuff
└── ...other files
```

The PostgreSQL database runs in a docker container and to start the API all you need to do is run:

```shell
make run
```

You might have to perform migrations:

```shell
make migrations
```

There is an API backend as well as a _nice_ looking frontend layout.

To run the frontend:

```shell
make run-frontend
```

## Lifter API Wrapper

[Here](https://github.com/WeightliftingNZ/lifter-api-wrapper) is an API wrapper implementation to allow ease of use with the RESTful framework.

[It is also available on PyPI](https://pypi.org/lifter-api-wrapper).

You can easily install it:

```sh

pip install lifter-api-wrapper

```
