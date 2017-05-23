import discord
import asyncio
import json
import os
import sys
from discord.ext import commands

bot = commands.Bot(command_prefix=".", description="Goku, the bot for the Nintendo Homebrew Idiot Log Discord!", pm_help=True)
    
@bot.event
async def on_ready():
    print('Bot launched successfully!')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------------')

@bot.event
async def on_message(message):
    if "freeshop" in message.content:
        await bot.delete_message(message)
        await bot.send_message(message.author, 'Please don\'t discuss piracy here.')
  
bot.load_extension("addons.commands")
  
bot.run('MzE2MDI3ODc4NjAzMDk2MDY1.DAPTiQ.7QG9qND8pAJWsvPcGuVqWmG2H3I')
