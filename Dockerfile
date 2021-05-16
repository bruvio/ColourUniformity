FROM python:3.7-slim

WORKDIR /usr/src/app


RUN apt update \
    && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1-mesa-dev

COPY ./requirements.txt ./

RUN python -m venv venv
RUN . venv/bin/activate \
    && pip install --upgrade pip
RUN . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt



COPY . .
RUN . venv/bin/activate \
    && pytest tests/ -s -v 



COPY . .
