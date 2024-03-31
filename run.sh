#!/bin/bash

docker build -t xizhuquan . && \
docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output xizhuquan
