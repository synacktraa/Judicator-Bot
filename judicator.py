import discord
import secrets
from discord.ext import commands


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")


@bot.event
async def on_raw_reaction_add(payload):
    """Gives a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != 947968073070161980:
        return

    guild = await bot.fetch_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    if str(payload.emoji) == "✅":
        role_id = 917940661901209650
    elif str(payload.emoji) == "❎":
        role_id = 936351416430256128
    else:
        role_id = None

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


@bot.command()
async def testing(ctx: commands.Context):
    await ctx.send("I hate my life!")



bot.run(secrets.OPEN_SOURCE_TOKEN)
