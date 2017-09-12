import discord
from discord.ext import commands

class Rules:

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command(pass_context=True, hidden=True)
    async def r1(self):
        await self.simple_embed("**1.** Don't mess with formatting for the log, even sorting of users. Rather, let <@177939404243992578> take care of it.")

    @commands.command(pass_context=True, hidden=True)
    async def r2(self):
        await self.simple_embed("**2.** Do not hold conversations anywhere on the log, the server works better for that, and formatting won't get screwed up.")
    
    @commands.command(pass_context=True, hidden=True)
    async def r3(self):
        await self.simple_embed("**3.** Please post any changes made to the log in <#318629676404834304>, so that changes can be followed easily.")
    @commands.command(pass_context=True, hidden=True)
    async def r4(self):
        await self.simple_embed("**4.** If you find a graph that shows the path an idiot on the log took, please get permission from the creator before adding it to the log, and cite the creator.")
    @commands.command(pass_context=True, hidden=True)
    async def r5(self):
        await self.simple_embed("**5.** Discuss in <#319940477732519938> additions to the log before adding them, as well as agree on a suitable rank for the person. Do not add people as you would like.")
    @commands.command(pass_context=True, hidden=True)
    async def r6(self):
        await self.simple_embed("**6.** If you would like the Neutron Stars role, you must have a total message count of 1,000 in #3ds-assistance-1 and #3ds-assistance-2 combined. DM <@316027878603096065> the image for the role.")
    @commands.command(pass_context=True, hidden=True)
    async def r7(self):
        await self.simple_embed("**7.** If you would like the Sheet Admins role, DM <@177939404243992578> a valid gmail. **Note: breaking any of the rules will result in you losing the role and ability to edit the log.**")
    @commands.command(pass_context=True, hidden=True)
    async def r8(self):
        await self.simple_embed("**8.** If you require support with a tech issue, you can do `.support` to access a channel where you can ask for help. `.unsupport` can be used to leave this channel.")
    @commands.command(pass_context=True, hidden=True)
    async def containment(self):
        await self.simple_embed("Please tag Tony Stark for access to the server after reading #rules so they can set you up with roles!")
        
    @commands.command(pass_context=True, hidden=True, aliases=['nick'])
    async def nickname(self):
        await self.simple_embed("If you would like a nickname, please DM it to @FuckFace McGee, and your nickname will be applied ASAP!")
        
    @commands.command(pass_context=True, hidden=True, aliases=['bu'])
    async def botuse(self):
        await self.simple_embed("**By participating in this server, you acknowledge that user data (including messages, user IDs, user tags) will be collected and logged for moderation purposes. If you disagree with this collection, please leave the server immediately.**")

def setup(bot):
    bot.add_cog(rules(bot))
