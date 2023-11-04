import discord
import logging

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
        self.confirmed = set()
        self.declined = set()
        self.maybe = set()
        
    @discord.ui.button(label='Yes', emoji="😎", style=discord.ButtonStyle.green)
    async def add_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add user name into message, if user clicked on 'yes' button.

        Args:
            interaction (discord.Interaction): Button interaction.
            button (discord.ui.Button): Discord button.
        """
        user = str(interaction.user).split("#")[0]
        self.confirmed.add(user)
        if user in self.declined:
            self.declined.remove(user)
        elif user in self.maybe:
            self.maybe.remove(user)
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
        self.declined.add(user)
        if user in self.confirmed:
            self.confirmed.remove(user)
        elif user in self.maybe:
            self.maybe.remove(user)
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
        self.maybe.add(user)
        if user in self.confirmed:
            self.confirmed.remove(user)
        elif user in self.declined:
            self.declined.remove(user)
        await self._set_fields()
        await interaction.response.edit_message(embed=self.embed)
        
    async def _set_fields(self):
        self.embed.set_field_at(index=3, name="Declined:", value='\n'.join(self.declined))
        self.embed.set_field_at(index=2, name="self.confirmed:", value='\n'.join(self.confirmed))
        self.embed.set_field_at(index=4, name="Maybe:", value='\n'.join(self.maybe))