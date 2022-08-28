FROM python:3.8

ARG DEPLOY_KEY

ENV APP_PATH=/code \
  PYTHONPATH=.

WORKDIR /root/.ssh

RUN echo $DEPLOY_KEY | base64 --decode > ./id_rsa \
  && ssh-keyscan github.com >> ./known_hosts \
  && chmod 600 ./*

WORKDIR $APP_PATH


RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y libgl1-mesa-dev poppler-utils poppler-data && \
  pip install poetry

COPY . .

RUN poetry install --no-dev

EXPOSE 8080

ENTRYPOINT ["poetry", "run"]
CMD ["python", "main.py"]
