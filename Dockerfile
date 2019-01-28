FROM ubuntu:18.04
LABEL author='Daniel Lee'

# Basic tools and configurations
RUN apt update
RUN apt install -y git vim wget curl locales screen
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Python installing
RUN apt install -y python3 python3-pip

# Bot moving
ADD . /home/telegram-bmstu-schedule-bot
WORKDIR /home/telegram-bmstu-schedule-bot

# Libs installation
RUN pip3 install -r requirements.txt
