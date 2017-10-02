import discord
from discord.ext import commands
import os
import sys
import json
import asyncio

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
    async def kick(self, ctx, member, *, reason=""):
        """Kick a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            try:
                await self.bot.send_message(found_member, "You have been kicked by user {0.name}#{0.discriminator}.\n{2}\nYou can rejoin the server with this link: https://discord.gg/hHHKPFz".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
            await self.bot.kick(found_member)
            await self.bot.say("Successfully kicked user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} kicked user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def ban(self, ctx, member, *, reason=""):
        """Ban a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await self.bot.send_message(found_member, "You have been banned by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this ban, send a direct message to one of the staff on the Server Admins list in {1}.\nIn the rare scenario that you do not have the entire staff list memorized, LyricLy#5752 and Griffin#2329 are two choices you could use.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            try: 
                await self.bot.send_message(found_member, "You have been banned by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this ban, send a direct message to one of the staff on the Server Admins list in {1}.\nIn the rare scenario that you do not have the entire staff list memorized, YourLocalLyric#5752 and Griffin#2329 are two choices you could use.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
            await self.bot.ban(found_member, 0)
            await self.bot.say("Successfully banned user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} banned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def mute(self, ctx, member, *, reason=""):
        """Mute a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.muted_role)
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await self.bot.say("Successfully muted user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} muted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "You have been muted by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this mute, send a direct message to one of the staff on the Server Admins list in {1}.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unmute(self, ctx, *, member):
        """Unmute a member."""
        found_member = self.find_user(member, ctx)
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if self.bot.muted_role in found_member.roles:
                await self.bot.remove_roles(found_member, self.bot.muted_role)
                embed = discord.Embed(description="{0.name}#{0.discriminator} unmuted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                await self.bot.send_message(found_member, "You have been unmuted by user {0.name}#{0.discriminator}. Don't do it again!".format(ctx.message.author))
                await self.bot.say("Successfully unmuted user {0.name}#{0.discriminator}!".format(found_member))
            else:
                await self.bot.say("That user isn't muted!")

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def uncontain(self, ctx, member):
        """Remove a member from #containment."""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.replace_roles(found_member, self.bot.unhelpful_jerks_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} moved user <@{1.id}> | {1.name}#{1.discriminator} out of <#335599294553915392>".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "Enjoy the server!")
            except discord.errors.Forbidden:
                pass
            
    @commands.has_permissions(kick_members=True)
    @commands.group(pass_context=True)
    async def promote(self, ctx):
        """Upgrade Roles"""
        if ctx.invoked_subcommand is None:
            message = await self.bot.say("You're missing a parameter!")
            await self.bot.delete_message(ctx.message)
            await asyncio.sleep(3)
            await self.bot.delete_message(message)

    @commands.has_permissions(kick_members=True)
    @promote.command(pass_context=True)
    async def Neutron(self, ctx, *, member):
        """Neutron Stars"""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            # await self.bot.replace_roles(found_member, self.bot.neutron_stars_role
            await self.bot.add_roles(found_member, self.bot.neutron_stars_role)
            await self.bot.remove_roles(found_member, self.bot.unhelpful_jerks_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Neutron Stars!".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "You're a Neutron Star now! Congrats, you're the densest known thing in the universe!")
            except discord.errors.Forbidden:
                pass

    @commands.has_permissions(kick_members=True)
    @promote.command(pass_context=True)
    async def Sheet(self, ctx, *, member):
        """Sheet Admins"""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.sheet_admin_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Sheet Admin!".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "You're a Sheet Admin now!")
            except discord.errors.Forbidden:
                pass

    @commands.has_permissions(ban_members=True)
    @promote.command(pass_context=True)
    async def Server(self, ctx, *, member):
        """Server Admins"""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.server_admin_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Server Admin!".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "You're a Server Admin now!")
            except discord.errors.Forbidden:
                pass
    
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def nosupport(self, ctx, member, *, reason="No reason given."):
        """Kicks a user out of support"""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        channel = self.bot.server.get_channel("336761748159987713")
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            if self.bot.support_role in found_member.roles:
                await self.bot.remove_roles(found_member, self.bot.support_role)
                overwrites = channel.overwrites_for(found_member)
                overwrites.read_messages = False
                await self.bot.edit_channel_permissions(channel, found_member, overwrites)
                embed = discord.Embed(description="{0.name}#{0.discriminator} kicked user <@{1.id}> | {1.name}#{1.discriminator} from <#336761748159987713>".format(ctx.message.author, found_member))
                embed.add_field(name="Reason given", value="• " + reason)
                await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
                try:
                    await self.bot.send_message(found_member, "You were removed from 9-1-1-tech-support by user {}#{}. The given reason was: `{}` \nIf you feel that you did not deserve this removal, send a direct message to one of the staff on the Server Admins list in <#318626746297745409>".format(ctx.message.author.name, ctx.message.author.discriminator, reason))
                except discord.errors.Forbidden:
                    pass
                await self.bot.say("{}#{} can no longer access support.".format(found_member.name, found_member.discriminator))
            else:
                await self.bot.say("That user isn't in support!")
                
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def givesupport(self, ctx, member):
        """Allows a user to rejoin support"""
        await self.bot.delete_message(ctx.message)
        found_member = self.find_user(member, ctx)
        channel = self.bot.server.get_channel("336761748159987713")
        if not found_member:
            await self.bot.say("That user could not be found.")
        else:
            await self.bot.add_roles(found_member, self.bot.support_role)
            overwrites = channel.overwrites_for(found_member)
            overwrites.read_messages = True
            await self.bot.edit_channel_permissions(channel, found_member, overwrites)
            embed = discord.Embed(description="{0.name}#{0.discriminator} restored user <@{1.id}> | {1.name}#{1.discriminator} permissions for <#336761748159987713>".format(ctx.message.author, found_member))
            await self.bot.send_message(self.bot.cmd_logs_channel, embed=embed)
            try:
                await self.bot.send_message(found_member, "You can access <#336761748159987713> again!")
            except discord.errors.Forbidden:
                pass
            await self.bot.say("{}#{} can access support again.".format(found_member.name, found_member.discriminator))
            
def setup(bot):
    bot.add_cog(Moderation(bot))
