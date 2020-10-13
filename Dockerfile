FROM ubuntu

COPY ./app /app

WORKDIR app

RUN apt update; yes Yes | apt install python3-pip;

RUN /bin/bash -c "pip3 install -r requirements.txt;"

RUN /bin/bash -c "apt install ncat -y;"

RUN /bin/bash -c "chmod +x ./entrypoint.sh"