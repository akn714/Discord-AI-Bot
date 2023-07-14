"""
### discord bot url ###
https://discord.com/api/oauth2/authorize?client_id=1128957735157899274&permissions=326417737728&scope=bot
"""


#!/usr/bin/env python3

# author: Adarsh Kumar (https://github.com/adarshkumar714)

import discord
import openai
import requests
import json
import os

openai.api_key = os.getenv('OPENAI_KEY')


def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + ' -' + json_data[0]['a']
        return quote
    except:
        print("[!] random quotes api is not working, need to fix it")
        return "SORRY NO QUOTE AVAILABLE !"

def get_joke():
    try:
        joke = requests.get('https://jokes-api.gamhcrew.repl.co/')
        return joke.text
    except:
        print("[!] random joke api is not working, need to fix it")
        return "SORRY NO JOKE AVAILABLE !"

def chat_gpt_get(content):
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [ 
                {"role": "user", "content": content}
            ]
        )["choices"][0]["message"]["content"] 
        return response
    except Exception as e:
        print("[!] Failed to get Chat-GPT reponse, need to fix it")
        print(e)
        return "SORRY SOME INTERNAL ERROR !"










from discord.ext import commands
import os

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())


@client.event
async def on_ready():
    print('we have logged in as %s'%client.user)
    # ...


@client.event
async def on_message(message):
    print(message)
    # ...

client.run('a446c58ebb655611de56b2a2162b83e3e1cfd4f09efc27c5b2ae83f8e7331514')
