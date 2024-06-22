#!/usr/bin/bash

# Stop container
docker stop mlsa-app-demo

# Remove container
docker rm mlsa-app-demo

# Remove image
docker image rm mlsa-app:demo

# Build image
docker build -f Dockerfile -t mlsa-app:demo .

# Run container
docker run -p 5000:5000 \
    --restart=always \
    --name mlsa-app-demo \
    -d mlsa-app:demo
