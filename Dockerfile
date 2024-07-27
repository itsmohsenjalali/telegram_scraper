FROM python:3.11

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Upgrading pip version
RUN pip install --upgrade pip

# Installing dependencies
RUN pip install gunicorn

COPY . .

# RUN pip freeze > requirements.txt

RUN pip install --no-cache-dir -r requirements.txt