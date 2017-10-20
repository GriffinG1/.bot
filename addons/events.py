import discord
from discord.ext import commands
import git


git = git.cmd.Git(".")
welcome_message = """
Welcome to the Nintendo Homebrew Idiot Log server! Please read our {} and have a ~~horrible~~ great time!
Please note we are in no way affiliated with the official Nintendo Homebrew server.

**By participating in this server, you acknowledge that user data (including messages, user IDs, user tags) will be collected and logged for moderation purposes. 
If you disagree with this collection, please leave the server immediately.**
"""

class Events:

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
            

    async def on_message(self, message):
        # auto update
        if message.author.name == "GitHub" and "git" in message.channel.name:
            print("Pulling changes!")
            git.pull()
            print("Changes pulled!")
            
        # receive private messages
        if isinstance(message.channel, discord.abc.PrivateChannel) and message.author.id != self.bot.user.id:
            embed = discord.Embed(description=message.content)
            if message.attachments:
                attachment_urls = []
                for attachment in message.attachments:
                    attachment_urls.append('[{}]({})'.format(attachment.filename, attachment.url))
                attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                embed.add_field(name='Attachments', value=attachment_msg, inline=False)
            await self.bot.private_messages_channel.send("Private message sent by {0.mention} | {0}:".format(message.author), embed=embed)
            
        # auto ban on 15+ pings
        if len(message.mentions) > 15:
            embed = discord.Embed(description=message.content)
            await message.delete()
            await message.author.kick()
            await message.channel.send("{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.logs_channnel.send("{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.logs_channel.send(embed=embed)

    async def on_message_delete(self, message):
        if isinstance(message.channel, discord.abc.GuildChannel) and message.author.id != self.bot.user.id:
            if message.channel not in (self.bot.msg_logs_channel, self.bot.containment_channel, self.bot.hidden_channel):
                if not message.content.startswith(tuple(self.bot.command_list), 1):
                    embed = discord.Embed(description=message.content)
                    if message.attachments:
                            attachment_urls = []
                            for attachment in message.attachments:
                                attachment_urls.append('[{}]({})'.format(attachment.filename, attachment.url))
                            attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                            embed.add_field(name='Attachments', value=attachment_msg, inline=False)
                    await self.bot.msg_logs_channel.send("Message by {0} deleted in channel {1.mention}:".format(message.author, message.channel), embed=embed)

    async def on_member_join(self, member):
        try:
            await member.send(welcome_message.format(self.bot.rules_channel.mention))
        except discord.errors.Forbidden:  # doesn't accept DMs from non-friends
            pass
        await member.add_roles(self.bot.idiots_role)
        embed = discord.Embed(title=":wave: Member joined", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        async for message in self.bot.blacklist_channel.history():
            if member.mention in message.content:
                embed.set_footer(text="This user is blacklisted.")
        await self.bot.logs_channel.send(":exclamation:", embed=embed)

    async def on_member_remove(self, member):
        embed = discord.Embed(title=":wave: Member left", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.logs_channel.send(":exclamation:", embed=embed)

    async def on_member_ban(self, guild, member):
        embed = discord.Embed(title=":anger: Member banned", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.logs_channel.send(":exclamation:", embed=embed)

    async def on_member_unban(self, guild, member):
        embed = discord.Embed(title=":anger: Member unbanned", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        await self.bot.logs_channel.send(":exclamation:", embed=embed)
        

def setup(bot):
    bot.add_cog(Events(bot))
