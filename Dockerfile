FROM python:3-slim
LABEL author='Daniel Lee'

RUN apt-get update -qq && apt-get install -y \
    curl \
    git \
    locales \
    screen \
    vim \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/

RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /home/telegram-bmstu-schedule-bot

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .
