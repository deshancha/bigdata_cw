ARG FLINK_VERSION

FROM flink:${FLINK_VERSION}-scala_2.12

# root is need for apt-get
USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip openjdk-11-jdk-headless && \
    ln -s /usr/bin/python3 /usr/bin/python

ARG FLINK_VERSION

# pyflink install
RUN export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::") && \
    pip3 install apache-flink==${FLINK_VERSION}

# default flink user
USER flink
