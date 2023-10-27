#!/usr/bin/env python3
import subprocess

# Step 1: Build the Docker image
build_command = "docker build --tag real_estate ./flask_app"
try:
    # Execute the build command and wait for it to finish
    subprocess.run(build_command, shell=True, check=True)
    print("Docker image build completed.")
except subprocess.CalledProcessError as e:
    print("Error building Docker image:", e)
    exit(1)

# Step 2: Start the Docker containers using docker-compose
compose_command = "docker-compose up -d "
try:
    # Execute the docker-compose command and wait for it to finish
    subprocess.run(compose_command, shell=True, check=True)
    print("Docker containers started successfully.")
except subprocess.CalledProcessError as e:
    print("Error starting Docker containers with docker-compose:", e)
    exit(1)