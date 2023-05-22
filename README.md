# How to run a project
Clone the project repository and navigate to the PyFlora directory.

Build and start the Docker containers using the following command:

```bash
docker-compose -f docker-compose.yaml up -d 
```
This command will start both the Flask app container and the API container that provides measurements for the Flask app.

Once the Docker containers are running, you can access the Flask app by opening the following URL in your browser:

* http://localhost:5000/ or http://127.0.0.1:5000/

Additionally, you can access the API documentation for the measurements API running inside the Docker container by visiting the following URL:

* http://localhost:8002/docs

# About
This project was created as the final assignment for the Python Professional Development Course from Algebra.

These instructions provide clear steps for running the project, including accessing the Flask app and the API documentation. It also provides a brief description of the project's purpose and origin.

