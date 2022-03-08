import discord
import secrets
import random
import platform  # For stats
import re
import lists
from discord.ext import commands

intents = discord.Intents.all()

#Bot activities
name_constant = "!help"
game_activity = discord.Game(name=name_constant)
streaming_activity = discord.Streaming(
    name=name_constant, url="https://www.twitch.tv")
listeting_activity = discord.Activity(
    type=discord.ActivityType.listening, name=name_constant)
watching_activity = discord.Activity(
    type=discord.ActivityType.watching, name=name_constant)

bot = commands.Bot(command_prefix='!', intents=intents,
                   status=discord.Status.online, help_command=None)
# Choose one of the activities
bot.activity = game_activity

bot.version = '1.5'

bot.colors = lists.BOT_COLORS
bot.color_list = [c for c in bot.colors.values()]


def censoring(message, patterns):
    """
        A recursive function which loops through the message and 
        checks for censored words until it is free of censored words
    """
    for pattern in patterns:
        edited = re.sub(r'\b{0}\b'.format(pattern),
                        f'{censor(pattern)}', message)

    return edited


def censor(pattern):
    temp = pattern
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    # replacing the vowels with an ascii character.
    for char in temp:
        for v in vowels:
            if char == v:
                temp = temp.replace(char, '\*')
    return temp


@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: !\n-----\nMy current activity:{bot.activity}\n-----")


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


@bot.event
async def on_message(message: discord.Message):
    """
        Checks for users messages.
    """
    if message.author == (bot.user or message.author.bot):
        return

    msg = message.content  # setting the msg variable to message content
    # channel variable to name of the channel in which message was sent
    channel = message.channel

    try:
        await bot.process_commands(message)
        """
            bot.process_commands processes the commands that have been registered to the bot and other groups. 
            Without this coroutine, none of the commands will be triggered.
        """
        # loops through the intents of possiblities json file
        patterns = lists.CENSORED
        outcome = censoring(msg, patterns)
        # bot deletes the message which contains the censored message & sends the edited message with the author name
        if outcome == msg:
            pass
        else:
            await message.delete()
            await channel.send(message.author.mention + f" Censored: {outcome} ")

    except discord.errors.NotFound:
        return

    except discord.ext.commands.errors.CommandNotFound:
        return


@bot.command(description="Ping-Pong game")
async def ping(ctx: commands.Context):
    await ctx.send("Pong! {0} ms".format(random.randrange(0, 1000)))


@bot.command(name='hi', aliases=['hello', 'yo'], description="Greets the user")
async def _hi(ctx):
    """
    A simple command which says hi to the author.
    """
    await ctx.send(f"Hi {ctx.author.mention}!")


@bot.command(aliases=['delete', 'purge'], description="Deletes the channels' message")
@commands.is_owner()
async def clear(ctx, lim: int):
    """
    this user defined bot function deletes the no. of messages provided by owner. Usage $clear <no.>
    """
    await ctx.channel.purge(limit=lim+1)


@clear.error
async def clear_error(ctx, error):
    """
    this function checks for error in the $clear command
    """

    if isinstance(error, commands.MissingRequiredArgument):
        # checks if an argument is missing
        await ctx.send("Usage: $clear <int>")
    elif isinstance(error, commands.BadArgument):
        # checks if the argument is integer value
        await ctx.send("Usage: $clear <int_val>")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.command(aliases=['disconnect', 'close', 'stopbot'], description="Turns off the bot")
@commands.is_owner()
async def logout(ctx):
    """
    If the user running the command owns the bot then this will disconnect the bot from discord.
    """
    await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
    await bot.logout()


@logout.error
async def logout_error(ctx, error):
    """
    Whenever the logout command has an error this will be tripped.
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.command(description="Shows bot information")
async def stats(ctx):
    """
    A usefull command that displays bot statistics.
    """
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(bot.guilds)
    member_count = len(set(bot.get_all_members()))

    embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=ctx.message.created_at)

    # embed.add_field(name='Bot Version:', value=bot.version)
    embed.add_field(name='Python Version:', value=python_version)
    embed.add_field(name='Discord.Py Version', value=dpy_version)
    embed.add_field(name='Total Guilds:', value=server_count)
    embed.add_field(name='Total Users:', value=member_count)
    embed.add_field(name='Bot Developers:',
                    value="<@503505263119040522>,<@453579828281475084>")

    embed.set_footer(text=f"{bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(description="Send information to specific channel.\nTakes 3 arguments: information,channel,title (always wrap in quotation marks)")
async def source(ctx: commands.Context, info, chan, topic):
    if chan not in lists.BLOCKED_CHANNELS:
        embed = discord.Embed(title=topic, description='\uFEFF',
                              colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.add_field(name="Information", value=info)
        guild = bot.get_guild(636962982286589952)
        for channel in guild.channels:
            if channel.name == chan:
                await ctx.message.delete()
                await channel.send(embed=embed)
                return
        await ctx.message.delete()
        await ctx.send("Channel not found!")
    else:
        await ctx.message.delete()
        await ctx.send("You are not able to write messages in " + chan + " channel!")


@source.error
async def source_error(ctx, error):
    """
    Whenever member uses command without arguments
    """
    if isinstance(error, commands.UserInputError):
        await ctx.send("Add missing arguments!")
    else:
        raise error


@bot.command(aliases=['channels'], description="Prints all available channels")
async def get_channels(ctx):
    output = "**Channels list:**\n|"
    guild = bot.get_guild(636962982286589952)
    for channel in guild.channels:
        if channel.name not in lists.BLOCKED_CHANNELS:
            output += channel.name+"|"
    await ctx.send(output)


@bot.command(name="help", description="Returns all available commands")
async def help(ctx: commands.Context):
    embed = discord.Embed(title=f'Available Commands:', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=ctx.message.created_at)
    for command in bot.commands:
        embed.add_field(name=f"{command}", value=command.description)
    await ctx.send(embed=embed)


bot.run(secrets.OPEN_SOURCE_TOKEN)
