ARG FLINK_VERSION

FROM flink:${FLINK_VERSION}-scala_2.12

# root is need for apt-get
USER root

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk-headless

# default flink user
USER flink
