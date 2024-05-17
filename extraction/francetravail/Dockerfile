FROM python:alpine3.19

WORKDIR /app
COPY requirements.txt requetage-api-date.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./requetage-api-date.py"]