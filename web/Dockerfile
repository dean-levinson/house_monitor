FROM ubuntu:latest 

WORKDIR /app/

ENV FLASK_DEBUG true 

EXPOSE 5000

RUN apt-get update && apt-get install -y python3-flask git

COPY requirements.txt .

RUN pip install --requirement ./requirements.txt

WORKDIR /app/src

COPY ./src .

CMD flask run -h 0.0.0.0
