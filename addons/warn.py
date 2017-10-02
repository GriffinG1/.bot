import discord
from discord.ext import commands
import os
import sys
import json
import asyncio

class Warning:
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
            
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def warn(self, ctx, member, *, reason="No reason given."):
        """Warn a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            owner = ctx.message.server.owner
            if self.bot.server_admin_role in found_member.roles and not ctx.message.author == owner:
                return await self.bot.say("You cannot warn a staff member!")
            try:
                self.warns[found_member.id]
            except KeyError:
                self.warns[found_member.id] = []
            self.warns[found_member.id].append(reason)
            reply_msg = "Warned user {}#{}. This is warn {}.".format(found_member.name, found_member.discriminator, len(self.warns[found_member.id]))
            private_message = "You have been warned by user {}#{}. The given reason was: `{}`\nThis is warn {}.".format(ctx.message.author.name, ctx.message.author.discriminator, reason, len(self.warns[found_member.id]))
            if len(self.warns[found_member.id]) >= 5:
                private_message += "\nYou were banned due to this warn.\nIIf you feel that you did not deserve this ban, send a direct message to one of the Server Admins.\nIn the rare scenario that you do not have the entire staff list memorized, you can DM <@177939404243992578> | Griffin#2329."
                try:
                    await self.bot.send_message(found_member, private_message)
                except discord.Forbidden:
                    pass
                await self.bot.ban(found_member)
                reply_msg += " As a result of this warn, the user was banned."
                
            elif len(self.warns[found_member.id]) == 4:
                private_message += "\nYou were kicked due to this warn.\nYou can rejoin the server with this link: https://discord.gg/hHHKPFz\nYour next warn will automatically ban you."
                try:
                    await self.bot.send_message(found_member, private_message)
                except discord.Forbidden:
                    pass
                await self.bot.kick(found_member)
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically ban the user."
                
            elif len(self.warns[found_member.id]) == 3:
                private_message += "\nYou were kicked due to this warn.\nYou can rejoin the server with this link: https://discord.gg/hHHKPFz\nYour next warn will automatically kick you."
                try:
                    await self.bot.send_message(found_member, private_message)
                except discord.Forbidden:
                    pass
                await self.bot.kick(found_member)
                reply_msg += " As a result of this warn, the user was kicked. The next warn will automatically kick the user."
                
            elif len(self.warns[found_member.id]) == 2:
                private_message += "\nYour next warn will automatically kick you."
                try:
                    await self.bot.send_message(found_member, private_message)
                except discord.Forbidden:
                    pass
                reply_msg += " The next warn will automatically kick the user."
                
            else:
                try:
                    await self.bot.send_message(found_member, private_message)
                except discord.Forbidden:
                    pass
            await self.bot.say(reply_msg)
            embed = discord.Embed(description="{0.name}#{0.discriminator} warned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            with open("saves/warns.json", "w+") as f:
                json.dump(self.warns, f)
                
    @commands.command(pass_context=True)
    async def listwarns(self, ctx, *, member=None):
        """List a member's warns."""
        if member is None:
            found_member = ctx.message.author
        elif member == "everyone":
            if ctx.message.author == ctx.message.server.owner:
                embed = discord.Embed(title="Warns for All Users", description="")
                for id in self.warns:
                    user_warns = self.warns[id]
                    if user_warns:
                        embed.description += "<@{}>\n".format(id)
                        for warn in user_warns:
                            embed.description += "• {}\n".format(warn)
                        embed.description += "\n"
                if embed.description is None:
                    await self.bot.say("There are no warns")
                else:
                    return await self.bot.say("", embed=embed)
            else:
                return await self.bot.say("Only the owner can check everyone's warns")
        else:
            found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if not ctx.message.author.server_permissions.ban_members and ctx.message.author != found_member:
                await self.bot.say("You don't have permission to use this command.")
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
        """Clear a member's warns."""
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
                    embed = discord.Embed(description="{0.name}#{0.discriminator} cleared warns of user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                    await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                    try:
                        await self.bot.send_message(found_member, "All your warns have been cleared.")
                    except discord.errors.Forbidden:
                        pass
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unwarn(self, ctx, member, *, reason):
        """Take a specific warn off a user."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:            
            try:
                if self.warns[found_member.id]:
                    try:
                        self.warns[found_member.id].remove(reason)
                        with open("saves/warns.json", "w+") as f:
                            json.dump(self.warns, f)
                        await self.bot.say("Removed `{}` warn of user {}#{}.".format(reason, found_member.name, found_member.discriminator))
                        embed = discord.Embed(description="{0.name}#{0.discriminator} took a warn off of user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                        embed.add_field(name="Removed Warn", value="• " + reason)
                        await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                    except ValueError:
                        await self.bot.say("{}#{} was never warned for the reason `{}`!".format(found_member.name, found_member.discriminator, reason))
                else:
                    await self.bot.say("That user has no warns!")
            except KeyError:
                await self.bot.say("That user has no warns!")
                
def setup(bot):
    bot.add_cog(Warning(bot))
