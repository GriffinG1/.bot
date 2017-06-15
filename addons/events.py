import discord
from discord.ext import commands
import git

git = git.cmd.Git(".")

class Events:
    """Event handling."""

    def __init__(self, bot):   
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    
    async def on_message(self, message):
        #filter "it seem"                                                  #thecommondude
        if message.content.startswith("it seem ") and message.author.id == "135204578986557440":
            await self.bot.send_message(message.channel, "STFU dude.")
            await self.bot.delete_message(message)
        #auto update 
        if message.author.name == "GitHub":
            print("Pulling changes!")
            git.pull()
            print("Changes pulled!")
        #recieve private messages
        if message.channel.is_private and message.author.id != self.bot.user.id:
            embed = discord.Embed(description=message.content)
            await self.bot.send_message(bot.private_messages_channel, "Private message sent by {}#{}:".format(message.author.name, message.author.discriminator), embed=embed)

    async def on_member_join(self, member):
        await self.bot.send_message(member, "Welcome to the official Nintendo Homebrew Idiot Log server! Please read our {} and have a ~~horrible~~ great time!".format(self.bot.rules_channel.mention))
        await self.bot.add_roles(member, self.bot.idiots_role)
        await self.bot.send_message(logs_channel, ":exclamation: Member join: {}#{}".format(member.name, member.discriminator))
        
    async def on_member_leave(self, member):
        await self.bot.send_message(logs_channel, ":exclamation: Member leave: {}#{}".format(member.name, member.discriminator))
        
def setup(bot):
    bot.add_cog(Events(bot))