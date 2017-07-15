import discord
from discord.ext import commands

class rules:

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command(pass_context=True)
    async def r1(self):
        await self.simple_embed("Don't mess with formatting for the log, even sorting of users. Rather, let <@177939404243992578> take care of it.")

    @commands.command(pass_context=True)
    async def r2(self):
        await self.simple_embed("Do not hold conversations anywhere on the log, the server works better for that, and formatting won't get screwed up.")
    
    @commands.command(pass_context=True)
    async def r3(self):
        await self.simple_embed("Please post any changes made to the log in <#318629676404834304>, so that changes can be followed easily.")
    @commands.command(pass_context=True)
    async def r4(self):
        await self.simple_embed("If you find a graph that shows the path an idiot on the log took, please get permission from the creator before adding it to the log, and cite the creator.")
    @commands.command(pass_context=True)
    async def r5(self):
        await self.simple_embed("Discuss in <#319940477732519938> additions to the log before adding them, as well as agree on a suitable rank for the person. Do not add people as you would like.")
    @commands.command(pass_context=True)
    async def r6(self):
        await self.simple_embed("If you would like the Neutron Stars role, you must have a total message count of 1,000 in #3ds-assistance-1 and #3ds-assistance-2 combined. DM <@316027878603096065> the image for the role.")
    @commands.command(pass_context=True)
    async def r7(self):
        await self.simple_embed("If you would like the Sheet Admins role, DM <@177939404243992578> a valid gmail. **Note: breaking any of the rules will result in you losing the role and ability to edit the log.**")

def setup(bot):
    bot.add_cog(rules(bot))