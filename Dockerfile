FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /kosl /repos

COPY requirements.txt /kosl

WORKDIR /kosl

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev postgresql-dev \
	&& pip install -r requirements.txt \
	&& apk del libffi-dev postgresql-dev

COPY . /kosl

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
