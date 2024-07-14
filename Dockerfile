FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask flask-sqlalchemy

RUN apk add --no-cache sqlite

EXPOSE 5001

CMD ["python", "app.py"]
