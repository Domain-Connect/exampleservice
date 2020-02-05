# Docker
Run the example service locally with the help of Docker.

## Build the service
Run the following after downloading for the first time or anytime the Dockerfile changes.
`docker-compose build`

## Start the service
You just start the webstack locally with the following.
`docker-compose up`

## Browse to the webpage
Add the local domain to your computer by editting your laptop's /etc/hosts file and add the following
`127.0.0.1 exampleservice.domainconnect.local`

Visit the following page in your browser.
http://exampleservice.domainconnect.local:8001

## Shell access
To log into bash shell in the python web app container
`docker-compose run web bash`

## Stop the local service
`docker-compose down`
