#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Adarsh Kumar (https://github.com/adarshkumar714)
"""
### discord bot url ###
https://discord.com/api/oauth2/authorize?client_id=1128957735157899274&permissions=326417737728&scope=bot
"""

from aibot import get_response

import discord
from discord.ext import commands
import requests
import os

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
"""
for storing chat histories for individual chats:

key -> unique chat id
value -> chat history for that chat
"""
history = dict()


def chat_history(user_id):
    global history
    try:
        return history[user_id]
    except:
        history[user_id] = []
        return history[user_id]


@client.event
async def on_ready():
    print('we have logged in as %s' % client.user)


@client.event
async def on_message(message):
    user_id = message.author
    query = message.content
    print(message)

    await message.channel.send('generating...')
    response, history[user_id] = get_response(query,
                                                   chat_history(user_id))
    await message.channel.send(response, reference=message)


def run_bot():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))


if __name__ == "__main__":
    run_bot()
