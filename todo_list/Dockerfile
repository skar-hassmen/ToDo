FROM python:3.10-alpine

WORKDIR /usr/src/todo_list

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirement.txt .
RUN pip install -r requirement.txt

COPY . .

ENTRYPOINT ["/usr/src/todo_list/entrypoint.sh"] 
