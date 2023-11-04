import discord
import logging

CONFIRMED = set()
DECLINED = set()
MAYBE = set()

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