FROM tsl0922/ttyd:alpine

#RUN apt-get update && apt install -y openssh-client && mkdir /root/.ssh && touch /root/.ssh/ssh_config

RUN apk add openssh-client && mkdir /root/.ssh && touch /root/.ssh/ssh_config
