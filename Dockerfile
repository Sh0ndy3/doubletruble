FROM ubuntu:latest
LABEL authors="kirch"

ENTRYPOINT ["top", "-b"]