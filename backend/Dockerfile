FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]