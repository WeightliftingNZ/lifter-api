# Lifter API

[![Build](https://github.com/ChristchurchCityWeightlifting/lifter-api/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/ChristchurchCityWeightlifting/lifter-api/actions/workflows/main.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a database of all lifts and competitions in the past, present and future.

## About

[Here is a video outlining the project](https://youtu.be/1kObqjeRs2I).

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

[Here](https://github.com/WeightliftingNZ/lifter-api-wrapper) is an API wrapper implementation to allow ease of use with the RESTful framework.

[It is also available on PyPI](https://pypi.org/lifter-api-wrapper).

You can easily install it:

```sh

pip install lifter-api-wrapper

```

## ToDos

| Release | Functionality                                                 | Time Required | Likely Delivery |
| ------- | ------------------------------------------------------------- | ------------- | --------------- |
| #1      | Import from OWLCMS and Excel results from 2022 onwards        | 1-2 months    | Sep/22          |
| #2      | Visual and usability review                                   | 1-2 months    | Sep/22          |
| #3      | Indication of Standards met based on comp results for lifters | 1-2 months    | Oct/22          |
| #4      | Lifter directory and history based on available results       | 3-4 months    | Jan/23          |
| #5      | Historical pre 2022 results import                            | 4-6 months    | Jun/23          |
| #6      | Records directory                                             | 3-4 months    | Aug/23          |
| #7      | Records integration with OWLCMS (currently in Alpha)          | 1-2 months    | ??              |

## Contribution

I will sort this out soon!
