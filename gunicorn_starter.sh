#!/bin/sh

gunicorn "run:create_app('$APP_SETTINGS')" -w ${GUNICORN_WORKERS:=2} -b 0.0.0.0:$PORT
