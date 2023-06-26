# syntax = docker/dockerfile:1.2.1

FROM python:3.8-buster
SHELL ["/bin/bash", "-c"]

COPY ./setup-scripts/system-requirements.sh /
RUN chmod +x /system-requirements.sh && /system-requirements.sh && rm /system-requirements.sh

RUN mkdir -p /root/.config/pip/
RUN --mount=type=secret,id=pipconf echo "$(cat /run/secrets/pipconf)" > /root/.config/pip/pip.conf

COPY ./requirements/dev.txt /opt/app/requirements/
COPY .flake8 .isort.cfg mypy.ini /opt/app/
COPY . /opt/app
COPY ./shared /opt/app/shared

RUN cd /opt/app \
 && make install-dev

WORKDIR /opt/app