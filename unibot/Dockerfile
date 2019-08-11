FROM ubuntu:latest
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev mongodb npm

ENV INSTALL_PATH /unibot
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH
COPY package.json .
RUN npm install

COPY . .

RUN pip3 install -r requirements.txt


ENTRYPOINT [ "python3"]

CMD ["index.py"]

