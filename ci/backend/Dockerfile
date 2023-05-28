FROM joyzoursky/python-chromedriver:3.8

LABEL maintainer="Dmitry Ermilov <dima74ermilov@gmail.com@gmail.com>"

# Dockerize
# https://github.com/jwilder/dockerize#ubuntu-images
RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# System packages
RUN pip install -U pip wheel


COPY app/requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt

VOLUME /var/app/
EXPOSE 8000
WORKDIR /var/app/

COPY ci/backend/entrypoint.sh /
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
