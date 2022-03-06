FROM python:3.8

ARG CLI_AWS_ACCESS_KEY_ID
ARG CLI_AWS_SECRET_ACCESS_KEY
ARG AWS_ROLE_ARN

ENV APP_PATH=/code \
    AWS_SDK_LOAD_CONFIG=1 \
    PYTHONPATH=.

ENV PATH="$APP_PATH/node_modules/.bin/:$PATH"

WORKDIR /root/.aws




ADD ./api $APP_PATH
WORKDIR $APP_PATH

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs
RUN pip install poetry

EXPOSE 3333
