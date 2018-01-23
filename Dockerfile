FROM python:2

run pip install websocket
run pip install websocket-client
run pip install slackclient

workdir /

add . /bot
add slack_token.txt /usr/local/etc
#cmd /bin/bash
cmd python /bot/src/main/python/bot.py

