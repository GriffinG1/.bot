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
    """Event handling."""

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_message(self, message):
        # filter "it seem"                                                 thecommondude
        if message.content.startswith("it seem ") and message.author.id == "135204578986557440":
            await self.bot.send_message(message.channel, "STFU dude.")
            await self.bot.delete_message(message)
            
        # auto update
        if message.author.name == "GitHub":
            print("Pulling changes!")
            git.pull()
            print("Changes pulled!")
            
        # recieve private messages
        if message.channel.is_private and message.author.id != self.bot.user.id:
            embed = discord.Embed(description=message.content)
            if message.attachments:
                attachment_urls = []
                for attachment in message.attachments:
                    attachment_urls.append('[{}]({})'.format(attachment['filename'], attachment['url']))
                attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                embed.add_field(name='Attachments', value=attachment_msg, inline=False)
            await self.bot.send_message(self.bot.private_messages_channel, 
                                        "Private message sent by {0.mention} | {0}:".format(message.author), embed=embed)
            
        # auto ban on 15+ pings
        if len(message.mentions) > 15:
            embed = discord.Embed(description=message.content)
            await self.bot.delete_message(message)
            await self.bot.kick_member(message.author)
            await self.bot.send_message(message.channel, "{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.send_message(self.bot.logs_channnel, "{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.send_message(self.bot.logs_channel, embed=embed)
        
                                        
    async def on_message_delete(self, message):
        if message.channel not in (self.bot.msg_logs_channel, self.bot.containment_channel, self.bot.hidden_channel):
            embed = discord.Embed(description=message.content)
            if message.attachments:
                    attachment_urls = []
                    for attachment in message.attachments:
                        attachment_urls.append('[{}]({})'.format(attachment['filename'], attachment['url']))
                    attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                    embed.add_field(name='Attachments', value=attachment_msg, inline=False)
            await self.bot.send_message(self.bot.msg_logs_channel, 
                                        "Message by {0} deleted in channel {1.mention}:".format(message.author, message.channel), embed=embed)

    async def on_member_join(self, member):
        try:
            await self.bot.send_message(member, welcome_message.format(self.bot.rules_channel.mention))
        except discord.errors.Forbidden:  # doesn't accept DMs from non-friends
            pass
        await self.bot.add_roles(member, self.bot.idiots_role)
        embed = discord.Embed(title=":wave: Member joined", description="<@{}> | {}#{} | {}".format(member.id, member.name, member.discriminator, member.id))
        async for message in self.bot.logs_from(blacklist_channel):
            if member.mention in message.content:
                embed.set_footer(text="This user is blacklisted.")
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
