import os
from os.path import join, dirname
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

# Initialize the dotEnv file & the discord bot.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='cad!')
token = os.environ.get("TOKEN")
botenabled = os.environ.get('DISCORD_BOT')

print(botenabled)
print("---------------")
print(token)

# Run the bot with the token from the dotEnv file.
bot.run(token=token)
