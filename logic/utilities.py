from logic import constants
import discord
from discord.ui import View


def replace_ic(data, pattern_to_be_replaced, new_pattern):
    """
        Replaces words while ignoring letters case.
    """
    idx = data.lower().find(pattern_to_be_replaced.lower())
    mod_data = data.replace(
        data[idx:idx+len(pattern_to_be_replaced)], new_pattern)
    return mod_data


def censor_message(msg):
    """
        Censors the message according to given patterns.
    """
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for pattern in constants.CENSORED:
        if pattern in msg.lower():
            rev_data = pattern
            for char in rev_data:
                for v in vowels:
                    if char == v:
                        rev_data = rev_data.replace(char, '\*')
            msg = replace_ic(msg, pattern, rev_data)
    return msg


class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅", custom_id="yes")
    async def button_yes_callback(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(917940661901209650)
        await interaction.user.add_roles(role)

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="❎", custom_id="no")
    async def button_no_callback(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(936351416430256128)
        await interaction.user.add_roles(role)
