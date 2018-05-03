FROM mkaichen/ubuntu-setup:bazel
ENV APP_DIR /usr/src/rast
WORKDIR $APP_DIR
COPY . $APP_DIR
RUN bazel build --spawn_strategy=standalone //...
RUN cp -Lr bazel-bin bin
RUN tar -czvf rast.tar.gz bin

FROM mkaichen/ubuntu-setup:python2
ENV APP_DIR /usr/src/rast
WORKDIR $APP_DIR
COPY --from=0 /usr/src/rast/rast.tar.gz .
RUN tar -xvf rast.tar.gz
RUN pip install pyyaml numpy

CMD [ "./bin/test" ]
