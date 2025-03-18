ARG REPO_NAME="georgelza"

FROM ${REPO_NAME}/ubuntu-openjdk8:24.04

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64

ENV HADOOP_VERSION=3.3.5
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/conf
ENV HADOOP_HEAPSIZE=1024

ENV MULTIHOMED_NETWORK=1
ENV PATH=$HADOOP_HOME/bin/:$PATH
ENV USER=root

USER root
WORKDIR /tmp/

RUN echo "--> Copy Source Binaries"
COPY stage/hadoop-$HADOOP_VERSION-aarch64.tar.gz /tmp

RUN echo "--> set environment variables"

RUN echo "--> install hadoop 3.3.5" && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION-aarch64.tar.gz && \
    mv /tmp/hadoop-$HADOOP_VERSION /opt/hadoop && \
    rm /tmp/hadoop-*

RUN echo "--> create symbolic link for hadoop" && \
    ln -s /opt/hadoop/etc/hadoop /etc/hadoop

RUN mkdir -p /opt/hadoop/logs
RUN mkdir -p /opt/hadoop/conf
RUN mkdir -p /hadoop-data

WORKDIR /opt/hadoop

ADD bin/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]