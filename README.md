# receipt-processing

This is the challenge to finish to build a webservice that fulfils the documented API.

## Skill

Python, Docker

## Set up
1. Installed:

- Ensure that you have [Docker](https://www.docker.com/) installed on your machine.
- Clone the project repository.

2.Build Docker:

- Dockerfile and requirements.txt exit
- Run the following command:

```
docker build -t receipts-app .
```

3. Run Docker:

```
docker run -d -p 5001:5000 receipts-app
```

4. Accessing the Application:

- The application will now be running in a Docker container and is accessible at local host.
- You can now use the defined routes to process receipts and retrieve points: http://localhost:xxxx/receipts/process for processing receipts and http://localhost:xxxx/receipts/{id}/points for retrieving points.

5. Stop and Remove Docker Container

## Test
Using the curl to test the endpoint
1. To test the `/receipts/process` endpoint with `curl`, you might use a command like this:
```
curl -X POST http://localhost:5001/receipts/process -H "recepit JSON bodoy"
```
2. To test the `/receipts/{id}/points` endpoint with `curl`, you might use a command like this:
```
curl http://localhost:5000/receipts/{id}/points
```
Replace the {id} with the actual ID returned from your /receipts/process endpoint.
