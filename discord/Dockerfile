FROM debian:bullseye

RUN apt-get update
RUN apt-get install -y apt-transport-https ca-certificates \
  openssl gpg gnupg2 software-properties-common curl wget \
  python3 python3-pycurl python3-apt python3-certifi

# Add CPOS deb repo to get the current version of discord.
RUN echo "deb [arch=amd64] https://darkmagus.dk/cpos/repo/ /" > /etc/apt/sources.list.d/cpos.list
RUN wget -q -O - https://darkmagus.dk/cpos/repo/CPOS.gpg | apt-key add -

RUN mkdir -p /build
WORKDIR /build

ENTRYPOINT ["python3", "docker-run.py"]
