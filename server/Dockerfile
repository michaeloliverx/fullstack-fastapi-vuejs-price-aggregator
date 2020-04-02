# --------------------------------------------------------------------------------
# `python-base` sets up all our shared environment variables
FROM python:3.8.1-slim-buster as python-base
    # python
    # prevent python buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    # prevent python writing pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    # disable pip cache
    PIP_NO_CACHE_DIR=off \
    # disable pip displaying message about new version
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # pinning poetry version
    POETRY_VERSION=1.1.0a1 \
    # where get-poetry script will install too
    POETRY_HOME="/opt/poetry" \
    # make poetry create venv in same dir as pyproject.toml
    # allows us to easily copy it later
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    # allow alembic to import our app
    PYTHONPATH="/app"

# add poetry + venv(so we don't have to activate it) to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
# --------------------------------------------------------------------------------



# --------------------------------------------------------------------------------
# `builder-base` is used to build prod python/system deps
# it will be used as a base for our dev builder too
FROM python-base as builder-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    # needed for GnuPG
    dirmngr \
    gnupg \
    \
    # for fetching things
    wget \
    curl \
    \
    # deps for building python deps
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# grab tini for signal processing and zombie killing
# https://github.com/krallin/tini
ENV TINI_VERSION 0.18.0
RUN set -x \
    && wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/v$TINI_VERSION/tini" \
    && wget -O /usr/local/bin/tini.asc "https://github.com/krallin/tini/releases/download/v$TINI_VERSION/tini.asc" \
    && gpg --batch --keyserver hkps://mattrobenolt-keyserver.global.ssl.fastly.net:443 --recv-keys 595E85A6B1B4779EA4DAAEC70B588DFF0527A9B7 \
    && gpg --batch --verify /usr/local/bin/tini.asc /usr/local/bin/tini \
    && rm /usr/local/bin/tini.asc \
    && chmod +x /usr/local/bin/tini

# install dockerize for waiting for other services to be available e.g. postgres
# https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION=0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/v$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-v$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-v$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-v$DOCKERIZE_VERSION.tar.gz

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# https://github.com/python-poetry/poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# copy project requirement files here to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./poetry.lock ./

# install python deps - respects $POETRY_VIRTUALENVS_IN_PROJECT
# only runtime deps installed, dev deps installed in later stage
RUN poetry install --no-dev
# --------------------------------------------------------------------------------


# --------------------------------------------------------------------------------
# `development-base` image is used to build dev deps
FROM builder-base as development-base
ENV FASTAPI_ENV=development
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# install the rest (dev) of our python deps
WORKDIR $PYSETUP_PATH
RUN poetry install
# --------------------------------------------------------------------------------



# --------------------------------------------------------------------------------
# `development` image used for local development
FROM builder-base as development
ENV FASTAPI_ENV=development

COPY --from=builder-base /usr/local/bin/dockerize /usr/local/bin/tini /usr/local/bin/
RUN true
COPY --from=development-base $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# /app will become the mountpoint for our code in development
WORKDIR /app

ENTRYPOINT exec tini -- /docker-entrypoint.sh $0 $@

CMD ["python", "manage.py", "develop"]
# --------------------------------------------------------------------------------



# --------------------------------------------------------------------------------
# `testing` image will be used for running tests / linters
FROM development as testing
ENV FASTAPI_ENV=testing \
    TESTING=true

# /app will become the mountpoint for our code in development
WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
# --------------------------------------------------------------------------------
