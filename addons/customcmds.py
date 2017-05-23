import discord
import json

the_filename = "customcmds.txt"
with open(the_filename) as f:
            comms = json.loads(f.readline().strip())

class CustomCmds:
    """Custom commands for Goku."""
    def __init__(self, bot):
        
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    
    async def on_message(self,message):
        if message.content.startswith('.add'):
            print("here")
            com = message.content.split(" ",2)
            print(com[1])
            print(com[2])
            comms.append([com[1],com[2]])
            print (str(comms))
            with open(the_filename, 'w') as f:
                f.write(json.dumps(comms))

        elif message.content.startswith('>'):
            for x in comms:
                if(message.content.split(" ")[0][1:] == x[0]):
                    await self.bot.send_message(message.channel,x[1])
def setup(bot):
    bot.add_cog(CustomCmds(bot))