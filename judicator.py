import discord
import secrets
import random
import platform
import constants
import utilities
import datetime
from types import SimpleNamespace
from discord.ext import commands
from discord.commands import Option


bot = commands.Bot(
    intents=discord.Intents.all(),
    status=discord.Status.streaming,
    activity=constants.ACTIVITIES['STREAM']
)
bot.colors = constants.BOT_COLORS
bot.color_list = SimpleNamespace(**bot.colors)


@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current activity:{bot.activity}\n-----")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """
        Gives a role based on a reaction emoji.
    """
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


@bot.event
async def on_message(message: discord.Message):
    """
        Checks for users messages.
    """
    if message.author == (bot.user or message.author.bot):
        return
    # Change to true if you want to enable censorship
    if constants.CENSORHIP_STATUS:
        channel = message.channel
        censored_message = utilities.censor_message(message.content)
        if message.content != censored_message:
            await message.delete()
            await channel.send(message.author.mention + f" Censored: {censored_message} ")


@bot.slash_command(description="Ping-Pong game.", guild_ids=[int(secrets.GUILD_ID)])
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! {random.randrange(0, 1000)} ms")


@bot.slash_command(description="Greets the user.", guild_ids=[int(secrets.GUILD_ID)])
async def hello(ctx: discord.ApplicationContext):
    """
        A simple command which says hi to the author.
    """
    await ctx.respond(f"Hi {ctx.author.mention}!")


@bot.slash_command(description="Deletes specified amount of messages from channel.", guild_ids=[int(secrets.GUILD_ID)])
@commands.is_owner()
async def clear(
    ctx: discord.ApplicationContext,
    limit: Option(int, "Enter number of messages")
):
    """
        Deletes number of messages specified by owner
    """
    await ctx.channel.purge(limit=limit)
    await ctx.respond("Channel cleared!")


@clear.error
async def clear_error(ctx: discord.ApplicationContext, error):
    """
        Error handler for cleaning function
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.slash_command(description="Turns off the bot.", guild_ids=[int(secrets.GUILD_ID)])
@commands.is_owner()
async def logout(ctx: discord.ApplicationContext):
    """
        If the user running the command owns the bot then this will disconnect the bot from discord.
    """
    await ctx.respond(f"Hey {ctx.author.mention}, I am now logging out :wave:")
    await bot.close()


@logout.error
async def logout_error(ctx: discord.ApplicationContext, error):
    """
        Whenever the logout command has an error this will be tripped.
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.slash_command(description="Shows bot information.", guild_ids=[int(secrets.GUILD_ID)])
async def stats(ctx: discord.ApplicationContext):
    """
        A usefull command that displays bot statistics.
    """
    embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Bot version:", value="2.0")
    embed.add_field(name='Python Version:', value=platform.python_version())
    embed.add_field(name='Discord.Py Version', value=discord.__version__)
    embed.add_field(name='Total Guilds:', value=str(len(bot.guilds)))
    embed.add_field(name='Total Users:', value=str(
        len(set(bot.get_all_members()))))
    embed.add_field(name='Bot owner:', value="<@503505263119040522>")
    embed.add_field(name='Bot Developers:',
                    value="<@503505263119040522>\n<@453579828281475084>\n<@890664690533957643>")
    embed.set_footer(text=f"{bot.user.name}",
                     icon_url=f"{bot.user.avatar.url}")
    await ctx.respond(embed=embed)


@bot.slash_command(description="Sends information to specific channel in beautiful block.", guild_ids=[int(secrets.GUILD_ID)])
async def post(
        ctx: discord.ApplicationContext,
        info: Option(str, "Enter your information"),
        channel: Option(discord.TextChannel, "Select a channel"),
        topic: Option(str, "Enter your title")
):
    temp = channel.name
    if temp not in constants.BLOCKED_CHANNELS:
        embed = discord.Embed(title=topic, description='\uFEFF',
                              colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Information", value=info)
        embed.set_footer(text=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar.url}")
        guild = bot.get_guild(int(secrets.GUILD_ID))
        for ch in guild.channels:
            if ch.name == temp:
                await ch.send(embed=embed)
                await ctx.respond("Message sent!")
                return
        await ctx.respond("Channel not found!")
    else:
        await ctx.respond("You are not able to write messages in " + temp + " channel!")


@bot.slash_command(description="Shows all available channels for post command.", guild_ids=[int(secrets.GUILD_ID)])
async def channels(ctx: discord.ApplicationContext):
    guild = bot.get_guild(int(secrets.GUILD_ID))
    embed = discord.Embed(title=f'Available Channels:', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
    for channel in guild.channels:
        if channel.name not in constants.BLOCKED_CHANNELS:
            embed.add_field(name=f"{channel.name}:", value=channel.topic)
    embed.set_footer(text=f"{ctx.author.name}",
                     icon_url=f"{ctx.author.avatar.url}")
    await ctx.respond(embed=embed)


@bot.slash_command(description="Shows all available commands.", guild_ids=[int(secrets.GUILD_ID)])
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title=f'Available Commands:', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
    # For some reason help command is repeated twice in the list.
    skip = 0
    for command in bot.application_commands:
        if command.description != "Shows all available commands.":
            embed.add_field(name=f"{command}:", value=command.description)
        else:
            if skip == 1:
                embed.add_field(name=f"{command}:", value=command.description)
            skip += 1
    embed.set_footer(text=f"{ctx.author.name}",
                     icon_url=f"{ctx.author.avatar.url}")
    await ctx.respond(embed=embed)


bot.run(secrets.OPEN_SOURCE_TOKEN)
