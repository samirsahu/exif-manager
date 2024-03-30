FROM python:3.12
# FROM ubuntu:latest

COPY docker-setup.sh requirements*.txt ./
RUN ./docker-setup.sh

WORKDIR /app