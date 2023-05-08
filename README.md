# How to run a project
Clone the project and navigate to the directory. Execute the following commands to build the Docker image from the Dockerfile.

After the image is built, run the Docker container with port 5000 exposed and in detached mode.

```bash
docker image build -t pyflora_docker .

docker run -p 5000:5000 -d pyflora_docker
```

Once the Docker container is running, go to the browser and enter the following URL:
http://localhost:5000/ or http://127.0.0.1:5000/

# About
This project is created as a final assignement for Python Professional Developmnet Course from Algebra

