FROM python:3.12.4

ARG PY_ENV

ENV PY_ENV=${PY_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3
  # ^^^
  # Make sure to update it!

# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
WORKDIR /pdi_rickandmorty
COPY poetry.lock pyproject.toml /pdi_rickandmorty/

# Project initialization:
RUN poetry install $(test "$PY_ENV" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /pdi_rickandmorty

# CMD ["streamlit", "run", "pdi_rickandmorty/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["poetry", "run", "python", "pdi_rickandmorty/main.py"]