import discord
from discord.ext import commands
import os
import sys
import json

class Moderation:
    """Bot commands for moderation."""
    def __init__(self, bot):
        self.bot = bot
        with open('saves/warns.json', 'r+') as f:
            self.warns = json.load(f)
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    def find_user(self, user, ctx):
        found_member = self.bot.server.get_member(user)
        if not found_member:
            found_member = self.bot.server.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        if not found_member:
            return None
        else:
            return found_member
    
    @commands.has_permissions(kick_members=True)    
    @commands.command(pass_context=True)
    async def kick(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.kick(found_member)
            await self.bot.say("Successfully kicked user {0.name}#{0.discriminator}!".format(found_member))
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def ban(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.ban(found_member)
            await self.bot.say("Successfully banned user {0.name}#{0.discriminator}!".format(found_member))
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def mute(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.muted_role)
            await self.bot.say("Successfully muted user {0.name}#{0.discriminator}!".format(found_member))
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unmute(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if self.bot.muted_role in found_member.roles:
                await self.bot.remove_roles(found_member, self.bot.muted_role)
                await self.bot.say("Successfully unmuted user {0.name}#{0.discriminator}!".format(found_member))
            else:
                await self.bot.say("That user isn't muted!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def warn(self, ctx, member, *, reason):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            try:
                self.warns[found_member.id]
            except KeyError:
                self.warns[found_member.id] = []
            self.warns[found_member.id].append(reason)
            reply_msg = "Warned user {}#{}. This was warn {}.".format(found_member.name, found_member.discriminator, len(self.warns[found_member.id]))
            if len(self.warns[found_member.id]) >= 5:
                await self.bot.ban(found_member)
                reply_msg += " As a result of this warn, the user was banned."
            elif len(self.warns[found_member.id]) >= 3:
                await self.bot.kick(found_member)
                reply_msg += " As a result of this warn, the user was kicked."
            if len(self.warns[found_member.id]) >= 4:
                reply_msg += " The next warn will automatically ban the user."
            elif len(self.warns[found_member.id]) >= 2:
                reply_msg += " The next warn will automatically kick the user."
            await self.bot.say(reply_msg)
            with open("saves/warns.json", "w+") as f:
                json.dump(self.warns, f)
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def listwarns(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            try:
                user_warns = self.warns[found_member.id]
                if user_warns:
                    embed = discord.Embed(title="Warns for user {}#{}".format(found_member.name, found_member.discriminator), description="")
                    for warn in user_warns:
                        embed.description += "• {}\n".format(warn)
                    embed.set_footer(text="There are {} warns in total.".format(len(user_warns)))
                    await self.bot.say("", embed=embed)
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, *, member):
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:            
            try:
                if self.warns[found_member.id]:
                    self.warns[found_member.id] = []
                    with open("saves/warns.json", "w+") as f:
                        json.dump(self.warns, f)
                    await self.bot.say("Cleared the warns of user {}#{}.".format(found_member.name, found_member.discriminator))
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
def setup(bot):
    bot.add_cog(Moderation(bot))
