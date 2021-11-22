FROM  python:3.9.7-slim

USER root
COPY . .

RUN pip install -r requirements.txt


