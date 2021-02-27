FROM python:3.9

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN pip install -U pip aiogram pytz pymongo pymongo[srv] loguru && apt-get update

COPY . .

ENTRYPOINT ["python", "main.py"]