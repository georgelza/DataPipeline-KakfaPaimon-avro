ARG REPO_NAME="georgelza"

FROM ${REPO_NAME}/apacheflink-base:1.19.1-scala_2.12-java11
SHELL ["/bin/bash", "-c"]

# this is where we have flink itself installed.
WORKDIR /opt/flink
ENV FLINK_HOME=/opt/flink

USER flink:flink

RUN echo "--> Install JARs: Flink's S3 plugin" && \
    mkdir ./plugins/s3-fs-hadoop && \
    mv ./opt/flink-s3-fs-hadoop-1.19.1.jar ./plugins/s3-fs-hadoop/

    
RUN mkdir -p /opt/flink/conf/
RUN mkdir -p /opt/flink/checkpoints
RUN mkdir -p /opt/flink/rocksdb


# Install JARs
# See https://repo.maven.apache.org/maven2/org/apache/flink/



RUN chown -R flink:flink /opt/flink

CMD ./bin/start-cluster.sh && sleep infinity
