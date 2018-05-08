FROM mkaichen/ubuntu-setup:bazel
ENV APP_DIR /usr/src/rast
WORKDIR $APP_DIR
COPY . $APP_DIR
RUN apt-get install -y python-pip
RUN easy_install pip

RUN pip install pyyaml numpy
RUN bazel build --spawn_strategy=standalone //...

RUN echo '#!/usr/bin/env bash\n\
bazel test //... --test_output=all\n\
bazel run //example:example' > docker_test.sh

CMD [ "bash", "docker_test.sh" ]
