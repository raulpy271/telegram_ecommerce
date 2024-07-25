FROM python:3.10-alpine3.19

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY . /app

CMD ["python", "bot.py"]
