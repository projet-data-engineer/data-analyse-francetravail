FROM python:alpine3.19

WORKDIR /app
COPY load_json_duckdb.py ./
RUN pip install duckdb

CMD [ "python", "./load_json_duckdb.py"]