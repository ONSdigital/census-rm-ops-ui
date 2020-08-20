FROM python:3.7-slim

EXPOSE 8234

RUN pip install pipenv

RUN groupadd --gid 1000 ops-ui && \
    useradd --create-home --system --uid 1000 --gid ops-ui ops-ui
WORKDIR /home/ops-ui
CMD ["./gunicorn_starter.sh"]

COPY Pipfile* /home/ops-ui/
RUN pipenv install --deploy --system
USER ops-ui

COPY --chown=ops-ui . /home/ops-ui
