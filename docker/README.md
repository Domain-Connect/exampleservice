# Docker
Run the example service locally with the help of Docker.

## Local Domain
Edit your laptop's /etc/hosts file and add the following
`127.0.0.1 exampleservice.domainconnect.local`

## Build
`docker-compose build`

## Start the service
`docker-compose up`

## Shell access
To log into bash shell in the python web app container
`docker-compose run web bash`

## To stop the containers
`docker-compose down`
