DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker build -t stoch:latest $DIR
#docker stop $(docker ps -a -q)
#docker rm $(docker ps -a -q)
#docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
