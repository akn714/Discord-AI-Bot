#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Adarsh Kumar (https://github.com/adarshkumar714)
"""
### discord bot url ###
https://discord.com/api/oauth2/authorize?client_id=1128957735157899274&permissions=326417737728&scope=bot
"""

# from aibot import get_response

import discord
from discord.ext import commands
from discord.utils import find
import requests
import os

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
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


@bot.event
async def on_ready():
    print('we have logged in as %s' % bot.user)

@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))

@bot.event
async def on_message(message):
    print(str(message.type))
    print('second', str(message.type)=='MessageType.new_member')
    if message.author!=bot.user and str(message.type) != 'MessageType.new_member':
        user_id = message.author
        query = message.content
        print('this is message after checking if a new user joins the server')
        # print(message)
    
        await message.channel.send('generating...')
        # response, history[user_id] = get_response(query, chat_history(user_id))
        response = f'this is the response {user_id}'
        await message.channel.send(response, reference=message)


def run_bot():
    bot.run(os.environ['DISCORD_BOT_TOKEN'])


if __name__ == "__main__":
    run_bot()
