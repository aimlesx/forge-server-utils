FROM alpine:3.19
COPY forge-1.20.1-47.2.20-installer.jar /mc/
RUN \
    cd /mc && \
    apk add openjdk17-jdk && \
    java -jar forge-1.20.1-47.2.20-installer.jar --installServer && \
    rm forge-1.20.1-47.2.20-installer.* && \
    echo "-XX:InitialRAMPercentage=50 -XX:MaxRAMPercentage=80" > user_jvm_args.txt
WORKDIR /mc
CMD ["./run.sh", "nogui"]