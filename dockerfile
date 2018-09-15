FROM ubuntu:18.04
LABEL author='Daniel Lee'

ENV REPO=github.com/BMSTU-bots/telegram-bmstu-schedule-bot

# Basic tools and configurations
RUN apt update
RUN apt install -y git vim wget curl locales
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# python installations
RUN apt install -y python3 python3-pip

# libs installation
RUN pip3 install bmstu-schedule pyTelegramBotAPI

# bot moving
ADD . /telegram-bmstu-schedule-bot
WORKDIR /telegram-bmstu-schedule-bot
RUN python3 bot.py