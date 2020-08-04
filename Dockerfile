FROM python:3.7-slim

ENV APP_SETTINGS=K8SDevelopmentConfig

WORKDIR /app
COPY . /app
EXPOSE 8003
RUN apt-get update -y && apt-get install -y python-pip curl git
RUN pip3 install pipenv && pipenv install --deploy --system
RUN apt-get remove -y --purge git

ENTRYPOINT ["python3"]
CMD ["run.py"]