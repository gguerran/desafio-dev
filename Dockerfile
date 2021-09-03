FROM python:3.9.5-alpine

RUN mkdir -p /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev openssl-dev libffi libffi-dev

RUN pip install --upgrade --no-cache pip
RUN pip install --no-cache-dir -r $APP_HOME/requirements.txt

RUN chmod 777 -R $APP_HOME