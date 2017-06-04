import discord
from discord.ext import commands

class Events:
    """Event handling."""

    def __init__(self, bot):   
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    
    async def on_message(self, message):
        #filter "it seem"
        if "it seem " in message.content and message.author.name == "thecommondude":
            await self.bot.send_message(message.channel, "STFU dude.")
            await self.bot.delete_message(message)
        #auto update 
        if message.author.name == "GitHub":
            print("Pulling changes!")
            git.pull()
            print("Changes pulled!")
        #recieve private messages
        if message.channel.is_private and message.author.id != bot.user.id:
            embed = discord.Embed(description=message.content)
            await self.bot.send_message(bot.private_messages_channel, "Private message sent by {}#{}:".format(message.author.name, message.author.discriminator), embed=embed)

    async def on_member_join(member):
        await bot.send_message(member, "Welcome to the official Nintendo Homebrew Idiot Log server! Please read our {} and have a ~~horrible~~ great time!".format(bot.rules_channel.mention))