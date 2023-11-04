from typing import Optional
import discord
from discord.ext import commands
import os
import asyncio
from datetime import date, datetime
import logging
import interactions
import re

from modules import SessionPlanner

CONFIRMED = set()
DECLINED = set()
MAYBE = set()

class ButtonView(discord.ui.View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        
    @discord.ui.button(label='Yes', emoji="😎", style=discord.ButtonStyle.green)
    async def count_is_going(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = str(interaction.user).split("#")[0]
        CONFIRMED.add(user)
        if user in DECLINED:
            DECLINED.remove(user)
        elif user in MAYBE:
            MAYBE.remove(user)
        self.embed.set_field_at(index=2, name="Confirmed:", value='\n'.join(CONFIRMED))
        self.embed.set_field_at(index=3, name="Declined:", value='\n'.join(DECLINED))
        self.embed.set_field_at(index=4, name="Maybe:", value='\n'.join(MAYBE))
        await interaction.response.edit_message(embed=self.embed)
        
    @discord.ui.button(label='No', emoji="😢", style=discord.ButtonStyle.red)
    async def count_is_not_going(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = str(interaction.user).split("#")[0]
        DECLINED.add(user)
        if user in CONFIRMED:
            CONFIRMED.remove(user)
        elif user in MAYBE:
            MAYBE.remove(user)
        self.embed.set_field_at(index=2, name="Confirmed:", value='\n'.join(CONFIRMED))
        self.embed.set_field_at(index=3, name="Declined:", value='\n'.join(DECLINED))
        self.embed.set_field_at(index=4, name="Maybe:", value='\n'.join(MAYBE))
        await interaction.response.edit_message(embed=self.embed)
        
    @discord.ui.button(label='Maybe', emoji="🤔", style=discord.ButtonStyle.gray)
    async def count_is_maybe_going(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = str(interaction.user).split("#")[0]
        MAYBE.add(user)
        if user in CONFIRMED:
            CONFIRMED.remove(user)
        elif user in DECLINED:
            DECLINED.remove(user)
        self.embed.set_field_at(index=3, name="Declined:", value='\n'.join(DECLINED))
        self.embed.set_field_at(index=2, name="Confirmed:", value='\n'.join(CONFIRMED))
        self.embed.set_field_at(index=4, name="Maybe:", value='\n'.join(MAYBE))
        await interaction.response.edit_message(embed=self.embed)
        

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", case_insensitive=True, strip_after_prefix=True, intents=intents)

@bot.command()
async def vote(ctx, *args):
    if "--from" in args:
        from_date = re.findall(r'\d+', args[args.index("--from")+1])
        from_date.reverse()
        from_date = date(*[int(i) for i in from_date])
    else:
        from_date = None
    if "--to" in args:
        to_date = re.findall(r'\d+', args[args.index("--to")+1])
        to_date.reverse()
        to_date = date(*[int(i) for i in to_date])
    else:
        to_date = None
    calendar = await create_calendar(from_date, to_date)
    embed = discord.Embed(title="Vote fot next session date!", color=discord.Color.dark_purple())
    await ctx.channel.send(embed=embed)
    for day in calendar:
        embed = discord.Embed(description=day, color=discord.Color.dark_purple())
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❔")
        await message.add_reaction("❌")

async def create_calendar(from_date, to_date):
    planner = SessionPlanner()
    planner.set_calendar(from_date, to_date)
    return planner.get_calendar()

@bot.command()
async def plan(ctx, *args):
    if "--date" in args:
        session_date = args[args.index("--date")+1]
    else:
        await ctx.channel.send("Please, give me date of the session.")
        return
    if "--name" in args:
        session_name = args[args.index("--name")+1]
    else:
        session_name = "Next session"
    if "--place" in args:
        session_place = args[args.index("--place")+1]
    else:
        session_place = "Somewhere"
    embed = discord.Embed(title=session_name, description="Are you going?", color=discord.Color.dark_purple())
    embed.add_field(name="When:", value=session_date, inline=False)
    embed.add_field(name="Where:", value=session_place, inline=False)
    embed.add_field(name="Confirmed:", value="", inline=False)
    embed.add_field(name="Declined:", value="", inline=False)
    embed.add_field(name="Maybe:", value="", inline=False)
    button = ButtonView(embed)
    message = await ctx.channel.send(embed=embed, view=button)
    await message.pin()
    
    
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))
    planner = SessionPlanner()