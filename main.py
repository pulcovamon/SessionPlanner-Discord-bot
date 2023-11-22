import discord
from discord.ext import commands
import os
import logging
import logging.handlers

from planner import SessionPlanner
from buttons import ButtonView

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", case_insensitive=True, strip_after_prefix=True, intents=intents)

@bot.command()
async def vote(ctx, *args):
    """Create voting calendar, when command 'vote' appears in messages.

    Args:
        ctx (discord.ext.commands.Context): Message context (metadata).
    """
    planner = SessionPlanner()
    await planner.set_calendar(*args)
    calendar = await planner.get_calendar()
    embed = discord.Embed(title="Vote fot next session date!", color=discord.Color.dark_purple())
    await ctx.channel.send(embed=embed)
    for embed in calendar:
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❔")
        await message.add_reaction("❌")
        
@bot.command()
async def plan(ctx, *args):
    """Create session event, when command 'vote' appears in messages.

    Args:
        ctx (discord.ext.commands.Context): Message context (metadata).
    """
    planner = SessionPlanner()
    if not await planner.set_session(*args):
        await ctx.channel.send("Please, give me date of the session.")
        return
    embed = await planner.get_session()
    button = ButtonView(embed)
    message = await ctx.channel.send(embed=embed, view=button)
    await message.pin()

    
if __name__ == "__main__":
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(os.path.dirname(__file__), "discord.log"),
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    bot.run(os.getenv('DISCORD_TOKEN'))
    planner = SessionPlanner()