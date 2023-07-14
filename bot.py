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


@client.event
async def on_ready():
    print('we have logged in as %s'%client.user)
    # ...


@client.event
async def on_message(message):
    print(message)
    # ...


client.run('a446c58ebb655611de56b2a2162b83e3e1cfd4f09efc27c5b2ae83f8e7331514')
