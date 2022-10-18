FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
WORKDIR /code

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pipenv pip
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --deploy --dev --skip-lock

COPY . /code/

RUN chmod +x /code/entrypoint.sh

CMD ["/bin/sh", "/code/entrypoint.sh"]

EXPOSE 8000
