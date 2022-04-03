# Lifter API

[![Build](https://github.com/ChristchurchCityWeightlifting/lifter-api/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/ChristchurchCityWeightlifting/lifter-api/actions/workflows/main.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a database of all lifts and competitions in the past, present and future!

## About

Instead of using .pdf's and Excel files to display competition results, I wanted to make a database for [Weightlifting New Zealand](https://weightlifting.nz). This allows more flexibility in reviewing results. Another bonus is that we can peek into an individual's athletic career.

## Local Development

Base requirements include:

- Docker v20.10.8
- Docker Compose v2.0.0
- Node v16.14.2
- Python v3.10.0

Here is the rough layout of the application:

```
lifter-api
├── backend/
│   ├── ... Django Rest Framework stuff
├── frontend
│   ├── ... React Typescript TailwindCSS stuff
└── ...other files
```

The PostgreSQL database runs in a docker container and to start the API all you need to do is run:

```
make run
```

You might have to perform migrations:

```
make migrations
```

There is an API backend as well as a _nice_ looking frontend layout.

To run the frontend:

```
make run-frontend
```

## Lifter API Wrapper

There is also a wrapper if you want to perform some cool data analytics!

[Check it out Lifter API Wrapper!](https://github.com/ChristchurchCityWeightlifting/lifter-api-wrapper).

[It is also available on PyPI!](https://pypi.org/lifter-api-wrapper)

You can easily install it:

```sh

pip install lifter-api-wrapper

```

## Contribution

I will sort this out soon. I'm currently working on an MVP.
