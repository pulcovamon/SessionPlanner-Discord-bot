import discord
from datetime import date, datetime
import logging
import re
from datetime import date, timedelta
from typing import Tuple, List

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