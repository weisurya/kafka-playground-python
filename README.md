# Kafka Playground with Python

## Requirements
- Python 3.7
- Docker

## PoC Architecture
![PoC Architecture](image/architecture.png)

## To run Kafka local:
- `docker-compose up -d --build`

## To run source-mongo:
- `cd source-mongo`
- `virtualenv -p <which python> venv`
- `source venv/bin/activate`
- `pip install -r requirement.txt`
- `python database.py`

## To run source-postgres:
- `create new database > run all sql statement on migration folder`
- `cd source-postgres`
- `virtualenv -p <which python> venv`
- `source venv/bin/activate`
- `pip install -r requirement.txt`
- `python database.py`

## To run source-kinesis:
- `cd source-kinesis`
- `virtualenv -p <which python> venv`
- `source venv/bin/activate`
- `pip install -r requirement.txt`
- `python kinesis.py`

## To run connector:

## To run consumer:
