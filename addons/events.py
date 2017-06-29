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
            await self.bot.send_message(self.bot.private_messages_channel, "Private message sent by {}#{}:".format(message.author.name, message.author.discriminator), embed=embed)

    async def on_member_join(self, member):
        try:
            await self.bot.send_message(member, "Welcome to the official Nintendo Homebrew Idiot Log server! Please read our {} and have a ~~horrible~~ great time!".format(self.bot.rules_channel.mention))
        except discord.errors.Forbidden: # doesn't accept DMs from non-friends
            pass
        await self.bot.add_roles(member, self.bot.idiots_role)
        embed = discord.Embed(title=":wave: Member joined", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.send_message(self.bot.logs_channel, ":exclamation:", embed=embed)

    async def on_member_remove(self, member):
        embed = discord.Embed(title=":wave: Member left", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.send_message(self.bot.logs_channel, ":exclamation:", embed=embed)

    async def on_member_ban(self, member):
        embed = discord.Embed(title=":anger: Member banned", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.send_message(self.bot.logs_channel, ":exclamation:", embed=embed)

    async def on_member_unban(self, server, member):
        embed = discord.Embed(title=":anger: Member unbanned", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.send_message(self.bot.logs_channel, ":exclamation:", embed=embed)
        

def setup(bot):
    bot.add_cog(Events(bot))
