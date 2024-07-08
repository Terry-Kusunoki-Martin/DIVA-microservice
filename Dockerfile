FROM alpine AS base

RUN apk update

RUN apk add curl bash unzip

RUN apk add python3 py3-pip

RUN apk add py3-urllib3

COPY get_resources.sh get_resources.sh

RUN ./get_resources.sh

FROM python:3.12-slim-bullseye

COPY --from=base /resources /resources

# jq and curl used for health check
# g++ and gcc used for python dependencies
RUN apt-get update && \
    apt-get install jq curl -y --no-install-recommends && \
    python -m pip install --upgrade --force pip

COPY requirements ./requirements

RUN pip install -r ./requirements/prod.txt

COPY service /service

RUN useradd -m -u 7777 apprunner && \
    chown -R apprunner /service /var/log

USER apprunner

CMD [ "python", "-m", "service.main" ]
