# syntax = docker/dockerfile:1.2.1
FROM python:3.8-buster AS builder
SHELL ["/bin/bash", "-c"]

RUN mkdir -p /root/.config/pip/
RUN --mount=type=secret,id=pipconf echo "$(cat /run/secrets/pipconf)" > /root/.config/pip/pip.conf

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

COPY ./requirements/prod.txt /opt/requirements/
COPY ./shared /opt/shared

RUN cd /opt \
 && pip install -r <(grep -v '^-e' requirements/prod.txt) 

 RUN cd /opt \
 && pip install --no-deps -r requirements/prod.txt

FROM python:3.8-slim-buster
EXPOSE 8080

COPY setup-scripts/system-requirements.sh /
RUN chmod +x /system-requirements.sh && /system-requirements.sh && rm /system-requirements.sh

COPY --from=builder /opt/venv /opt/venv
COPY ./src /opt/src

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /opt

COPY setup-scripts/docker-entrypoint.sh .
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "sh", "./docker-entrypoint.sh" ]