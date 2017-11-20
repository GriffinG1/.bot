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
    async def test(self, ctx):
        """A test command."""
        servers = ""
        embed = discord.Embed(title="testing", description="Testing")
        embed.add_field(name="Notes", value="Testing!", inline=False)
        for x in self.bot.guilds:
            servers += x.name + " " + str(x.id) + "\n"
        embed.add_field(name="Notes", value=servers, inline=False)
        embed.colour = discord.Colour(0x00FFFF)            
        await ctx.send(embed=embed)
    
    @commands.command()
    async def snoop(self, ctx):
        """whee"""
        members = ""
        for x in self.bot.guilds:
            if x.id == 381991923004735489:
                for y in x.members:
                    members += y.name + " " + str(y.id) + "\n"
                members += "Owner ==" + x.owner.name + " " + str(x.owner.id)
        await ctx.send(members)

    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def restart(self, ctx):
        """Restarts the bot."""
        await ctx.send("Restarting...")
        with open("restart.txt", "w+") as f:
            f.write(str(ctx.message.channel.id))
            f.close()
        sys.exit(0)

    @commands.command()
    async def support(self, ctx):
        """Use to access the support channel"""
        await ctx.message.delete()
        found_member = ctx.message.author
        member_roles = found_member.roles
        if not self.bot.support_role in member_roles:
            await found_member.add_roles(self.bot.support_role)
            embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} accessed <#336761748159987713>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You now have access to <#336761748159987713>")
            except discord.errors.Forbidden:
                pass
        else:
            await found_member.remove_roles(self.bot.support_role)
            embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} left <#336761748159987713>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You have left <#336761748159987713>")
            except discord.errors.Forbidden:
                pass
            
    @commands.command()
    async def about(self, ctx):
        """Information about Goku"""
        embed = discord.Embed(description="Goku is a shitty bot created by <@177939404243992578> for use on the Nintendo Homebrew Idiot Log server. \nYou can view the source code [here](https://github.com/GriffinG1/Goku/)")
        await ctx.send(embed=embed)
            
    @commands.command()
    async def derek(self, ctx):
        """Get your Daily Derek today!"""
        await ctx.message.delete()
        found_member = ctx.message.author
        member_roles = found_member.roles
        if not self.bot.derek_role in member_roles:
            await found_member.add_roles(self.bot.derek_role)
            embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} has chosen to meme about <#357720803988733952>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You can now meme about derek in <#357720803988733952>!")
            except discord.errors.Forbidden:
                pass
        else:
            await found_member.remove_roles(self.bot.derek_role)
            embed = discord.Embed(description="<@{1.id}> | {0.name}#{0.discriminator} has chosen to leave <#357720803988733952>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You don't want to derek meme anymore?")
            except discord.errors.Forbidden:
                pass
            
def setup(bot):
    bot.add_cog(Utility(bot))
