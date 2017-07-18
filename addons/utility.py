import discord
from discord.ext import commands
import os
import sys

class Utility:
    """Utility bot commands."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
    
    @commands.command()
    async def test(self):
        """A test command."""
        embed = discord.Embed(title="testing", description="Testing")
        embed.add_field(name="Notes", value="Testing!", inline=False)
        embed.colour = discord.Colour(0x00FFFF)            
        await self.bot.say("", embed=embed)

    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def restart(self):
        """Restarts the bot."""
        await self.bot.say("Restarting...")
        sys.exit(0)

    @commands.command(pass_context=True)
    async def support(self, ctx):
        """Use to access the support channel"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.add_roles(found_member, self.bot.support_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} accessed <#336761748159987713>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You now have access to <#336761748159987713>")
        except discord.errors.Forbidden:
            pass
            
    @commands.command(pass_context=True)
    async def unsupport(self, ctx):
        """Use to remove access to the support channel"""
        await self.bot.delete_message(ctx.message)
        found_member = ctx.message.author
        member_roles = found_member.roles
        await self.bot.remove_roles(found_member, self.bot.support_role)
        embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} left <#336761748159987713>".format(ctx.message.author, found_member))
        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
        try:
            await self.bot.send_message(found_member, "You have left <#336761748159987713>")
        except discord.errors.Forbidden:
            pass
            
def setup(bot):
    bot.add_cog(Utility(bot))
