import discord
import secrets
from discord.ext import commands
from discord import Game

intents = discord.Intents.all()

help_command = commands.DefaultHelpCommand(
    no_category='Commands'
)

bot = commands.Bot(command_prefix='!', description='Testing Commands',
                   help_command=help_command, intents=intents)


@bot.command()
async def testing(ctx: commands.Context):
    await ctx.send("I hate my life!")


@bot.event
async def on_ready():
    print("Logged in as "+str(bot.user.name))


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ID of the message that can be reacted to to add/remove a role.
        self.role_message_id = 947968073070161980
        self.emoji_to_role = {
            # ID of the role associated with unicode emoji '✅'.
            discord.PartialEmoji(name='✅'): 917940661901209650,
            # ID of the role associated with unicode emoji '❎'.
            discord.PartialEmoji(name='❎'): 936351416430256128,
        }

    @bot.event
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


bot.run(secrets.OPEN_SOURCE_TOKEN)
