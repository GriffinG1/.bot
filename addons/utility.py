import discord
from discord.ext import commands
import os
import sys
import datetime

class Utility:
    """Utility bot commands."""
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
    
    @commands.has_permissions(ban_members=True)
    @commands.group()
    async def joins(self, ctx):
        """Checks joins.txt"""
        if ctx.invoked_subcommand is None:
            with open("joins.txt") as f:
                joins = f.read()
            if len(joins) == 0:
                await ctx.send("Joins.txt is empty!")
            elif len(joins) < 2000:
                await ctx.send(joins)
            else:
                await ctx.send("File is over 2000 characters, please get the file manually from T3CHNOLOG1C")
    
    @commands.has_permissions(ban_members=True)
    @joins.command()
    async def clear(self, ctx):
        """Clears joins.txt"""
        open("joins.txt", "w+")
        await ctx.send("Cleared joins.txt")
    
    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.channel)
    @commands.command(aliases=['test'])
    async def ping(self, ctx):
        await ctx.message.delete()
        """Get response time."""
        msgtime = ctx.message.created_at.now()
        await (await self.bot.ws.ping())
        now = datetime.datetime.now()
        ping = now - msgtime
        await ctx.send("🏓 Response Time: **{}ms**".format(ping.microseconds / 1000.0))
        
    @commands.has_permissions(ban_members=True)    
    @commands.command()
    async def restart(self, ctx):
        """Restarts the bot."""
        await ctx.send("Restarting...")
        with open("restart.txt", "w+") as f:
            f.write(str(ctx.message.channel.id))
            f.close()
        sys.exit(0)
        
    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def pull(self, ctx):
        """Pull GitHub changes"""
        await ctx.send("Pulling changes...")
        git.pull()
        await ctx.send("Changes pulled! Restarting...")
        with open("restart.txt", "w+") as f:
            f.write(str(ctx.message.channel.id))
            f.close()
        sys.exit(0)
            
    @commands.command()
    async def about(self, ctx):
        """Information about .bot"""
        embed = discord.Embed(description=".bot is a shitty bot created by <@177939404243992578> for use on the Nintendo Homebrew Idiot Log server. \nYou can view the source code [here](https://github.com/GriffinG1/.bot/)")
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Utility(bot))
