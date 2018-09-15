FROM ubuntu:18.04
LABEL author='Daniel Lee'

# Basic tools and configurations
RUN apt update
RUN apt install -y git vim wget curl locales screen
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# python installations
RUN apt install -y python3 python3-pip

# libs installation
RUN pip3 install bmstu-schedule pyTelegramBotAPI

# bot moving
ADD . /home/telegram-bmstu-schedule-bot
WORKDIR /home/telegram-bmstu-schedule-bot
RUN mkdir vault/