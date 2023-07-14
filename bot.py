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


def chat_history(key):
  global history
  try:
    return history[key]
  except:
    history[key] = []
    return history[key]


@bot.event
async def on_ready():
  print('we have logged in as %s' % bot.user)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  # for conversations
  key = ""
  query = message.content

  if message.content == "?reset_history":
    history[key] = []
    await message.channel.send('Conversation history reset done')
    return

  # direct messages
  if str(message.channel) == 'Direct Message with Unknown User':
    print('[+] DM', f'from {message.author}')
    key = message.channel.id
    # await message.channel.send('generating response...')
    chats = chat_history(key)
    response, chats = get_response(query, chats)
    history[key] = chats

  # channel messages
  else:
    print('[+] messages in channels')
    if str(message.type) == 'MessageType.new_member':
      await message.channel.send(f'Hello {message.author}', reference=message)
    if message.author != bot.user and str(
        message.type) != 'MessageType.new_member':
      # await message.channel.send('generating response...')
      chats = chat_history(key)
      response, chats = get_response(query, chats)
      history[key] = chats

  # final response
  await message.channel.send(response[0].page_content, reference=message)


def run_bot():
  bot.run(os.environ['DISCORD_BOT_TOKEN'])


if __name__ == "__main__":
  run_bot()
