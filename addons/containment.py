import discord
import asyncio
import os
import sys
from discord.ext import commands

class Containment:
    """Functions to manage the containment channel."""
    def __init__(self, bot):
        self.bot = bot
        self.countdown = 0
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
    
    async def containment_loop(self):
        await self.bot.wait_until_ready()
        await self.bot.wait_until_login()
        while self is self.bot.get_cog("Containment"):
            await asyncio.sleep(1)
            self.countdown += 1
            if self.countdown == 90:
                deleted_message = False
                async for message in self.bot.containment_channel.history(limit=500):
                    if not (message.content == "Please tag Tony Stark for access to the server after reading <#318626746297745409> so they can set you up with roles!" and self.bot.user == message.author):
                        await message.delete()
            
    async def on_message(self, message):
        if message.channel == self.bot.containment_channel:
            self.countdown = 0
        
def setup(bot):
    containment = Containment(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(containment.containment_loop())
    bot.add_cog(containment)