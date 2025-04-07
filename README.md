
## Deploying a Flask App to a Linux Server with Docker

This guide explains how to deploy a Flask application to a Linux server using Docker.

---

## Prerequisites

- A Linux server (e.g., Ubuntu)
- Docker installed on the server
- The project files (including dependencies list)

---

## Building a docker image

1. Write a docker file that copies the relevant project files and dependencies to the target directory.

2. Build the docker image using - 
```bash
docker build -t myflaskapp .
```

## Running the server 
Once the image is built, run the app using:

```bash
docker run -d -p 5000:5000 --name flask-server my-flask-app
```

> For advanced deployment, consider using kubernetes for loads managment, routing and security.**