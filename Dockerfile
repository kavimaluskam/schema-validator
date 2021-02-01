FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

ADD . /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD python cli.py