# Pull base image
FROM python:3.12.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN pip install fastapi uvicorn psycopg2 sqlalchemy requests

COPY . /code/

EXPOSE 8000