import discord
from discord.ext import commands

class Rules:

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True)
    async def r1(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "1." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r2(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "2." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r3(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "3." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r4(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "4." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r5(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "5." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r6(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "6." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r7(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "7." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def r8(self, ctx):
        embed = discord.Embed()
        async for rule in self.bot.rules_channel.history():
            if "8." in rule.content:
                embed.description = rule.content
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def containment(self, ctx):
        await ctx.message.delete()
        if self.bot.sheet_admin_role in ctx.author.roles or self.bot.server_admin_role in ctx.author.roles or self.bot.nazi_role in ctx.author.roles:
            await ctx.send("Please tag Tony Stark for access to the server after reading <#318626746297745409> so they can set you up with roles!")
        else:
            await ctx.send("You can't use this command!", delete_after=5)
        
    @commands.command(hidden=True, aliases=['nick'])
    async def nickname(self, ctx):
        embed = discord.Embed(description="If you would like a nickname, please DM it to <@366483552788938772>, and your nickname will be applied ASAP!")
        await ctx.send(embed=embed)
        
    @commands.command(hidden=True, aliases=['bu'])
    async def botuse(self, ctx):
        embed = discord.Embed(description="**By participating in this server, you acknowledge that user data (including messages, user IDs, user tags) will be collected and logged for moderation purposes. If you disagree with this collection, please leave the server immediately.**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Rules(bot))
