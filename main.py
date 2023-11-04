import discord
from discord.ext import commands
import os
import logging

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
    bot.run(os.getenv('DISCORD_TOKEN'))
    planner = SessionPlanner()