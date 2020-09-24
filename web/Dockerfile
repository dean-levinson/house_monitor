FROM ubuntu:latest 

WORKDIR /app/

ENV FLASK_DEBUG true 

EXPOSE 5000

RUN apt-get update && apt-get install -y python3-flask git python3-pip

COPY requirements.txt .

RUN pip3 install --requirement ./requirements.txt

COPY ./src ./src

WORKDIR /app/src

CMD flask run -h 0.0.0.0
