#!/usr/bin/bash

# Stop container
docker stop mlsa-app-1

# Remove container
docker rm mlsa-app-1

# Remove image
docker image rm mlsa-app:v1

# Build image
docker build -f Dockerfile -t mlsa-app:v1 .

# Run container
docker run -p 5000:5000 \
    --restart=always \
    --name mlsa-app-1 \
    -d mlsa-app:v1
