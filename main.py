import discord
from discord.ext import commands
import os
from datetime import date, datetime
import logging
import re
from datetime import date, timedelta
from typing import Tuple, List

CONFIRMED = set()
DECLINED = set()
MAYBE = set()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", case_insensitive=True, strip_after_prefix=True, intents=intents)

class SessionPlanner(object):
    """Allow to create session message and voting message.
    """
    def __new__(cls):
        """It is singleton.

        Returns:
            SessionPlanner: Instance of this class.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionPlanner, cls).__new__(cls)
        return cls.instance
    
    async def _format_date(self, argument: str, *args: Tuple[str]) -> datetime.date:
        """Get date from message text.

        Args:
            argument (str): Which argument specifies if it is 'start date' of 'end date'.

        Returns:
            datetime.date: date in right format.
        """
        current_date = re.findall(r'\d+', args[args.index(argument)+1])
        current_date.reverse()
        current_date = date(*[int(i) for i in current_date])
        return current_date

    async def set_calendar(self, *args: Tuple[str]):
        """Set start date and end date of the voting calendar.
        """
        if "--from" in args:
            from_date = await self._format_date("--from", *args)
        else:
            from_date = date.today() + timedelta(days=1)
        if "--to" in args:
            to_date = await self._format_date("--to", *args)
        else:
            to_date = from_date + timedelta(days=7)
        self.calendar = []
        delta = timedelta(days=1)
        while from_date <= to_date:
            self.calendar.append(from_date)
            from_date += delta

    async def get_calendar(self) -> List[discord.Embed]:
        """Return all days from the calendar in message format.

        Returns:
            List[discord.Embed]: Objects, which can be used to send message.
        """
        if not self.calendar:
            return None
        embeds = []
        space = "\u00A0"
        for day in self.calendar:
            day_text = f"{day.strftime('%A')}{space}{day.day}.{space}{day.month}.{space}{day.year}"
            embeds.append(discord.Embed(description=day_text, color=discord.Color.dark_purple()))
        return embeds
    
    async def set_session(self, *args: Tuple[str]) -> bool:
        """Sets session variables like date, name and place.

        Returns:
            bool: It returns False if session cannot be set due to no date in args.
        """
        if "--date" in args:
            self.session_date = args[args.index("--date")+1]
        else:
            return False
        if "--name" in args:
            self.session_name = args[args.index("--name")+1]
        else:
            self.session_name = "Next session"
        if "--place" in args: 
            self.session_place = args[args.index("--place")+1]
        else:
            self.session_place = "Somewhere"
        return True
        
    async def get_session(self) -> discord.Embed:
        """Return session characteristics in proper format.

        Returns:
            discord.Embed: Session characteristics, which can be send in message.
        """
        embed = discord.Embed(title=self.session_name, description="Are you going?", color=discord.Color.dark_purple())
        embed.add_field(name="When:", value=self.session_date, inline=False)
        embed.add_field(name="Where:", value=self.session_place, inline=False)
        embed.add_field(name="Confirmed:", value="", inline=False)
        embed.add_field(name="Declined:", value="", inline=False)
        embed.add_field(name="Maybe:", value="", inline=False)
        return embed

class ButtonView(discord.ui.View):
    """Allow to add buttons to a message.
    """
    def __init__(self, embed: discord.Embed):
        """Not a singleton.

        Args:
            embed (discord.Embed): Object, which can be sent in message.
        """
        super().__init__()
        self.embed = embed
        
    @discord.ui.button(label='Yes', emoji="😎", style=discord.ButtonStyle.green)
    async def add_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add user name into message, if user clicked on 'yes' button.

        Args:
            interaction (discord.Interaction): Button interaction.
            button (discord.ui.Button): Discord button.
        """
        user = str(interaction.user).split("#")[0]
        CONFIRMED.add(user)
        if user in DECLINED:
            DECLINED.remove(user)
        elif user in MAYBE:
            MAYBE.remove(user)
        await self._set_fields()
        await interaction.response.edit_message(embed=self.embed)
        
    @discord.ui.button(label='No', emoji="😢", style=discord.ButtonStyle.red)
    async def add_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add user name into message, if user clicked on 'no' button.

        Args:
            interaction (discord.Interaction): Button interaction.
            button (discord.ui.Button): Discord button.
        """

        user = str(interaction.user).split("#")[0]
        DECLINED.add(user)
        if user in CONFIRMED:
            CONFIRMED.remove(user)
        elif user in MAYBE:
            MAYBE.remove(user)
        await self._set_fields()
        await interaction.response.edit_message(embed=self.embed)
        
    @discord.ui.button(label='Maybe', emoji="🤔", style=discord.ButtonStyle.gray)
    async def add_maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add user name into message, if user clicked on 'maybe' button.

        Args:
            interaction (discord.Interaction): Button interaction.
            button (discord.ui.Button): Discord button.
        """

        user = str(interaction.user).split("#")[0]
        MAYBE.add(user)
        if user in CONFIRMED:
            CONFIRMED.remove(user)
        elif user in DECLINED:
            DECLINED.remove(user)
        await self._set_fields()
        await interaction.response.edit_message(embed=self.embed)
        
    async def _set_fields(self):
        self.embed.set_field_at(index=3, name="Declined:", value='\n'.join(DECLINED))
        self.embed.set_field_at(index=2, name="Confirmed:", value='\n'.join(CONFIRMED))
        self.embed.set_field_at(index=4, name="Maybe:", value='\n'.join(MAYBE))
        

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