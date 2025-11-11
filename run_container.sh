#!/bin/bash
# Rebuild and run the Library Management System container

echo "Building and starting the container..."
docker-compose down

docker-compose up --build