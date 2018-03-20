# stop and remove the existing containers
docker-compose stop
docker-compose rm -f

# up and run the container
docker-compose build
docker-compose up -d

docker-compose exec account_administration bash


