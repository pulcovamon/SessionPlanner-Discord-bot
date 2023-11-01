import discord
import os
import asyncio
from datetime import date, datetime

from modules import SessionPlanner

client = discord.Client(intents=discord.Intents(messages=True, guilds=True, message_content=True, ))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)
    if message.content.startswith('$plan session'):
        message_text = message.content.strip().split(" ")
        if "from" in message_text:
            from_index = message_text.index("from")
            from_date = date(*[int(message_text[i].replace(".", "")) for i in range(from_index+3, from_index, -1)])
        else:
            from_date = None
        if "to" in message_text:
            to_index = message_text.index("to")
            to_date = date(*[int(message_text[i].replace(".", "")) for i in range(to_index+3, to_index, -1)])
        else:
            to_date = None
        planner = SessionPlanner(from_date, to_date)
        print(planner)
        embed = discord.Embed(title="Vote for next session date!", description=planner.get_calendar(), color=0x206694, timestamp=datetime.today())
        embed.set_footer(text=f"{message.author}")
        new_message = await message.channel.send(embed=embed)
        new_message.add_reaction("✅")
        await asyncio.sleep(5)

client.run(os.getenv('DISCORD_TOKEN'))