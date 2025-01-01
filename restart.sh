#!/bin/bash

# Stop and remove containers, networks, images, and volumes
docker-compose down

# Remove all unused containers, networks, volumes, and images not referenced by any containers-
docker system prune -af

# Build and run your docker-compose services
docker compose up -d --build
