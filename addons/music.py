import discord
from discord.ext import commands
import os
import sys

class Music:
    """Bot commands for playing music."""
    def __init__(self, bot):
        self.bot = bot
        self.voice_channel = None
        self.player = None
        print('Addon "{}" loaded'.format(self.__class__.__name__))  
  
    @commands.group(pass_context=True)
    async def music(self, ctx):
        """Music commands."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("You need to tell me more than that, mate. How do you expect me to know what to do if you just tell me 'music'? I might as well join a random voice channel and start playing Rick Astley's Never Gonna Give You Up. Think about your actions, okay? Thank you.")
            
    @music.command(pass_context=True)
    async def join(self, ctx):
        """Join a voice channel."""
        if ctx.message.author.voice.voice_channel:
            self.voice_channel = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            await self.bot.say("Successfully joined your voice channel!")
        else:
            await self.bot.say("You're not in a voice channel. Man, I try my best, but sometimes you make it so difficult. I can't tell what to join when you're not in a server. Please, just give me something to work with.")
            
    @music.command()
    async def leave(self):
        """Leave a voice channel."""
        if self.bot.server.get_member(self.bot.user.id).voice.voice_channel:
            voice_client = self.bot.voice_client_in(ctx.message.server)
            await voice_client.disconnect()
            await self.bot.say("Successfully left voice!")
        else:
            await self.bot.say("*sigh* I'm not in a voice channel. You're asking me to do things that I just can't do. You expect too much of me. I put in such an effort, but sometimes...")
            
    @music.command()
    async def play(self, url):
        """Play a YouTube URL in voice chat."""
        print(self.voice_channel)
        if self.voice_channel:
            self.player = await self.voice_channel.create_ytdl_player(url)
            self.player.start()
        else:
            await self.bot.say("How am I supposed to play music when I'm not in a voice channel? *Think. Think. Think.* Please.")
            
    @music.command()
    async def stop(self):
        """Stop a playing song."""
        if self.player:
            if self.player.is_playing():
                self.player.stop()
                self.player = None
            else:
                await self.bot.say("I'm not PLAYING a song! Ugh!")
        else:
            await self.bot.say("I'm not PLAYING a song! Ugh!")

def setup(bot):
    bot.add_cog(Music(bot))
