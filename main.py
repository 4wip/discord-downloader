import discord
from discord.ext import commands
import os
import aiohttp

bot = commands.Bot(command_prefix='>', self_bot=True)

@bot.command()
async def dl(ctx, server_id: str = None):    

        server = bot.get_guild(int(server_id))
        if not server:
            return
            
        async with aiohttp.ClientSession() as session:
            for channel in server.channels:
                if isinstance(channel, discord.TextChannel):
                    try:
                        async for message in channel.history(limit=None):
                            for attachment in message.attachments:
                                path = os.path.join('media', attachment.filename)
                                if not os.path.exists(path):
                                    async with session.get(attachment.url) as resp:
                                        if resp.status == 200:
                                            with open(path, 'wb') as f:
                                                f.write(await resp.read())
                                            print(f"{attachment.filename}")
                    except discord.Forbidden:
                        continue
                
bot.run('token')
