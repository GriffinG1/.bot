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
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    def find_user(self, user, ctx):
        found_member = self.bot.guild.get_member(user)
        if not found_member:
            found_member = self.bot.guild.get_member_named(user)
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
    async def kick(self, ctx, member, *, reason="No reason was given."):
        """Kick a member."""
        found_member = self.find_user(member, ctx)
        if found_member == ctx.message.author:
            return await ctx.send("You can't kick yourself, you absolute fucking dumbass.")
        elif not found_member:
            await ctx.send("That user could not be found.")
        else:
            if reason != "No reason was given.":
                reason_msg = "The given reason was: {}".format(reason)
            try:
                await found_member.send("You have been kicked by user {0.name}#{0.discriminator}.\n{2}\nYou can rejoin the server with this link: https://discord.gg/hHHKPFz".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
            await found_member.kick()
            await ctx.send("Successfully kicked user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} kicked user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.cmd_logs_channel.send(embed=embed)
    
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def ban(self, ctx, member, *, reason="No reason was given."):
        """Ban a member."""
        found_member = self.find_user(member, ctx)
        if found_member == ctx.message.author:
            return await ctx.send("You can't ban yourself, you fuckwad.")
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            if reason != "No reason was given.":
                reason_msg = "The given reason was: {}".format(reason)
            try: 
                await found_member.send("You have been banned by user {}#{}.\n{}\nIf you feel that you did not deserve this ban, send a direct message to one of the Server Admins.\nIn the rare scenario that you do not have the entire staff list memorized, you can DM <@177939404243992578> | Griffin#2329.".format(ctx.message.author.name, ctx.message.author.discriminator, reason_msg))
            except discord.errors.Forbidden:
                pass
            await self.bot.guild.ban(found_member, delete_message_days=0)
            await ctx.send("Successfully banned user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} banned user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• " + reason)
            await self.bot.cmd_logs_channel.send(embed=embed)
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def mute(self, ctx, member, *, reason=""):
        """Mute a member."""
        found_member = self.find_user(member, ctx)
        if found_member == ctx.message.author:
            return await ctx.send("Why the fuck are you trying to mute yourself?!?!?!")
        elif not found_member:
            await ctx.send("That user could not be found.")
        else:
            await found_member.add_roles(self.bot.muted_role)
            if reason:
                reason_msg = "The given reason was: {}".format(reason)
            else:
                reason_msg = "No reason was given."
            await ctx.send("Successfully muted user {0.name}#{0.discriminator}!".format(found_member))
            embed = discord.Embed(description="<@{0.id}> | {0.name}#{0.discriminator} muted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
            embed.add_field(name="Reason given", value="• {}".format(reason if reason else "*no reason given*"))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You have been muted by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this mute, send a direct message to one of the staff on the Server Admins list in {1}.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
            
    @commands.has_permissions(ban_members=True)    
    @commands.command(pass_context=True)
    async def unmute(self, ctx, *, member):
        """Unmute a member."""
        found_member = self.find_user(member, ctx)
        if found_member == ctx.message.author:
            await ctx.send("How did you manage to mute yourself...")
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            if self.bot.muted_role in found_member.roles:
                await found_member.remove_roles(self.bot.muted_role)
                embed = discord.Embed(description="{0.name}#{0.discriminator} unmuted user <@{1.id}> | {1.name}#{1.discriminator}".format(ctx.message.author, found_member))
                await self.bot.cmd_logs_channel.send(embed=embed)
                await found_member.send("You have been unmuted by user {0.name}#{0.discriminator}. Don't do it again!".format(ctx.message.author))
                await ctx.send("Successfully unmuted user {0.name}#{0.discriminator}!".format(found_member))
            else:
                await ctx.send("That user isn't muted!")

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def uncontain(self, ctx, member):
        """Remove a member from #containment."""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            await found_member.add_roles(self.bot.unhelpful_jerks_role)
            await found_member.remove_roles(self.bot.idiots_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} moved user <@{1.id}> | {1.name}#{1.discriminator} out of <#335599294553915392>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("Enjoy the server!")
            except discord.errors.Forbidden:
                pass
            
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def recontain(self, ctx, member, reason="No reason was given."):
        """Put a member back in #containment."""
        await ctx.message.delete()
        rolelist = ""
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if found_member == ctx.message.author:
            return await ctx.send("You can't contain yourself, fucknugget.")
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            for role in member_roles:
                rolelist += "•{}\n".format(role)
            found_member.edit(roles=[])
            await found_member.add_roles(self.bot.idiots_role)
            embed = discord.Embed(description="{}#{} recontained user {} | {}#{} for \n•{}. Users roles were:\n{}".format(ctx.message.author.name, ctx.message.author.discriminator, found_member.mention, found_member.name, found_member.discriminator, reason, rolelist))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You have been recontained by user {0.name}#{0.discriminator}.\n{2}\nIf you feel that you did not deserve this mute, send a direct message to one of the staff on the Server Admins list in {1}.".format(ctx.message.author, self.bot.rules_channel.mention, reason_msg))
            except discord.errors.Forbidden:
                pass
        
            
    @commands.has_permissions(kick_members=True)
    @commands.group(pass_context=True)
    async def promote(self, ctx):
        """Upgrade Roles"""
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send("You're missing a parameter!", delete_after=3)

    @commands.has_permissions(kick_members=True)
    @promote.command(pass_context=True)
    async def Neutron(self, ctx, *, member):
        """Neutron Stars"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            await found_member.add_roles(self.bot.neutron_stars_role)
            await found_member.remove_roles(self.bot.unhelpful_jerks_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Neutron Stars!".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You're a Neutron Star now! Congrats, you're the densest known thing in the universe!")
            except discord.errors.Forbidden:
                pass

    @commands.has_permissions(kick_members=True)
    @promote.command(pass_context=True)
    async def Sheet(self, ctx, *, member):
        """Sheet Admins"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            await found_member.add_roles(self.bot.sheet_admin_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Sheet Admin!".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You're a Sheet Admin now!")
            except discord.errors.Forbidden:
                pass

    @commands.has_permissions(ban_members=True)
    @promote.command(pass_context=True)
    async def Server(self, ctx, *, member):
        """Server Admins"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        member_roles = found_member.roles
        if not found_member:
            ctx.send("That user could not be found.")
        else:
            await found_member.add_roles(self.bot.server_admin_role)
            embed = discord.Embed(description="{0.name}#{0.discriminator} promoted user <@{1.id}> | {1.name}#{1.discriminator} to Server Admin!".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You're a Server Admin now!")
            except discord.errors.Forbidden:
                pass
    
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def nosupport(self, ctx, member, *, reason="No reason given."):
        """Kicks a user out of support"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        channel = self.bot.guild.get_channel(336761748159987713)
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            if self.bot.support_role in found_member.roles:
                await found_member.remove_roles(self.bot.support_role)
                await channel.set_permissions(found_member, read_messages=False)
                embed = discord.Embed(description="{0.name}#{0.discriminator} kicked user <@{1.id}> | {1.name}#{1.discriminator} from <#336761748159987713>".format(ctx.message.author, found_member))
                embed.add_field(name="Reason given", value="• " + reason)
                await self.bot.cmd_logs_channel.send(embed=embed)
                try:
                    await found_member.send("You were removed from 9-1-1-tech-support by user {}#{}. The given reason was: `{}` \nIf you feel that you did not deserve this removal, send a direct message to one of the staff on the Server Admins list in <#318626746297745409>".format(ctx.message.author.name, ctx.message.author.discriminator, reason))
                except discord.errors.Forbidden:
                    pass
                await ctx.send("{}#{} can no longer access support.".format(found_member.name, found_member.discriminator))
            else:
                await ctx.send("That user isn't in support!")
                
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def givesupport(self, ctx, member):
        """Allows a user to rejoin support"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        channel = self.bot.guild.get_channel(336761748159987713)
        if not found_member:
            await ctx.send("That user could not be found.")
        else:
            await channel.set_permissions(found_member, read_messages=True)
            embed = discord.Embed(description="{0.name}#{0.discriminator} restored user <@{1.id}> | {1.name}#{1.discriminator} permissions for <#336761748159987713>".format(ctx.message.author, found_member))
            await self.bot.cmd_logs_channel.send(embed=embed)
            try:
                await found_member.send("You can access <#336761748159987713> again!")
            except discord.errors.Forbidden:
                pass
            await ctx.send("{}#{} can access support again.".format(found_member.name, found_member.discriminator))
            
def setup(bot):
    bot.add_cog(Moderation(bot))
