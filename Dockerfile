FROM mkaichen/ubuntu-setup:bazel
ENV APP_DIR /usr/src/rast
WORKDIR $APP_DIR
COPY . $APP_DIR
RUN apt-get install -y python-pip
RUN easy_install pip

RUN pip install pyyaml numpy
RUN bazel build --spawn_strategy=standalone //...

CMD [ "bash", "test.sh" ]
