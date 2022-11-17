# python 3.7.x: 1-15 - https://peps.python.org/pep-0537/
# python 3.8.x: 1-15 - https://peps.python.org/pep-0569/
# python 3.9.x: 1-15 - https://peps.python.org/pep-0596/
# python 3.10.x: 1-8 - https://peps.python.org/pep-0619/

docker build -t spotflow --build-arg VERSION=3.8.0 .

docker create --name dummy spotflow
docker cp dummy:/app/v.txt .

docker rm -f dummy
docker image rm -f spotflow
