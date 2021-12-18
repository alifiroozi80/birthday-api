FROM python:3.9.6

WORKDIR /app

RUN apt -y update
#RUN apk update

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "server.py"]
