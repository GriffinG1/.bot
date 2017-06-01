import discord
import json
from discord.ext import commands

class Log:
    """
    Log commands for the Nintendo Homebrew Idiot Log server.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)
        
    @commands.group()
    async def log(self):
        """Command for managing the bot's idiot log with subcommands."""
    
    @commands.has_permissions(administrator=True)    
    @log.command()
    async def add(self, name, rank, identifier, first_seen="N/A", last_seen="N/A", nickname="N/A", banned="no", notes="N/A"):
        #make sure the rank is one of the five valid ranks
        if rank == "Diamond" or rank == "Platinum" or rank == "Gold" or rank == "Silver" or rank == "Bronze":
            #replace spaces with underscores and save into name_var
            name_var = ""
            for letter in name:
                if letter == " ":
                    name_var += "_"
                else:
                    name_var += letter
            name_var = name_var.lower()
            #create dictionary with data from command
            new_entry = {
                "name": name,
                "rank": rank,
                "identifier": identifier,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "nickname": nickname,
                "banned": banned,
                "notes": notes
            }
            #load log.json into data, add previously created dictonary and write back to the file
            with open('log.json', 'r+') as f:
                data = json.load(f)
            data[name_var] = new_entry
            with open('log.json', 'w+') as f:
                json.dump(data, f)
            await self.bot.say("Successfully added {} to the log!".format(name))
        else:
            await self.bot.say(rank + " is not a valid rank. Must be: Diamond, Platinum, Gold, Silver, Bronze")
        
    @log.command()
    async def view(self, name):
        with open('log.json', 'r+') as f:
            data = json.load(f)
        #iterate through file looking for an entry that matches input
        user = {}
        for entry in data:
            if data[entry]["name"].lower() == name.lower():
                user = data[entry]
        #if entry couldn't be found, send an error
        if not user:
            await self.bot.say(name + " is not an entry in the idiot log.")
        #otherwise create an embed with the information from the entry and send a message
        else:
            embed = discord.Embed(title=user["name"], description="Rank: {}\nIdentifier: {}\nFirst seen: {}\nLast seen: {}\nBanned: {}\nNickname: {}".format(user["rank"], user["identifier"], user["first_seen"], user["last_seen"], user["banned"], user["nickname"]))
            if not user["notes"] == "N/A":
                embed.add_field(name="Notes", value=user["notes"], inline=False)
            if user["rank"] == "Diamond":
                embed.colour = discord.Colour(0x00FFFF)
            elif user["rank"] == "Platinum":
                embed.colour = discord.Colour(0xBFD7FF)
            elif user["rank"] == "Gold":
                embed.colour = discord.Colour(0xF1C232)
            elif user["rank"] == "Silver":
                embed.colour = discord.Colour(0xCCCCCC)
            elif user["rank"] == "Bronze":
                embed.colour = discord.Colour(0xE69138)
            await self.bot.say("", embed=embed)
        with open('log.json', 'w+') as f:
            json.dump(data, f)
    
    @commands.has_permissions(administrator=True)  
    @log.command()
    async def remove(self, name):
        with open('log.json', 'r+') as f:
            data = json.load(f)
        #iterate through file looking for an entry that matches input
        delete_entry = None
        for entry in data:
            if data[entry]["name"].lower() == name.lower():
                 delete_entry = entry
        if delete_entry == None:
            await self.bot.say(name + " is not an entry in the idiot log.")
        #then delete it
        else:
            data.pop(delete_entry, None)
            await self.bot.say(name + " was successfully removed from the idiot log.")
        with open('log.json', 'w+') as f:
            json.dump(data, f)
            
    @log.command()
    async def edit(self, name, key, value):
        with open('log.json', 'r+') as f:
            data = json.load(f)
        #iterate through file looking for an entry that matches input
        user = None
        for entry in data:
            if data[entry]["name"].lower() == name.lower():
                 user = data[entry]
        if key in user:
            await self.bot.say("Successfully edited {}'s {} field to {}!".format(user["name"], key, value))
        else:
            await self.bot.say("Invalid field. Entries have 'name', 'rank', 'identifier', 'first_seen', 'last_seen', 'nickname' and 'notes' fields.")
        with open('log.json', 'w+') as f:
            json.dump(data, f)
        
    
def setup(bot):
    bot.add_cog(Log(bot))