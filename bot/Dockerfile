FROM python:3.8

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip install -r requirements.txt

WORKDIR /code
COPY . /code
COPY .env /code
ADD .env ./
CMD ["python", "bot.py"]