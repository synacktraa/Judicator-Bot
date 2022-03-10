import discord
import secrets
import random
import platform
import re
import lists
from discord.ext import commands
from discord.commands import Option

intents = discord.Intents.all()

# Bot activities
name_constant = "/help"
game_activity = discord.Game(name=name_constant)
streaming_activity = discord.Streaming(
    name=name_constant, url="https://www.twitch.tv")
listeting_activity = discord.Activity(
    type=discord.ActivityType.listening, name=name_constant)
watching_activity = discord.Activity(
    type=discord.ActivityType.watching, name=name_constant)

bot = commands.Bot(
    intents=intents, status=discord.Status.online, help_command=None)

# Choose one of the activities
bot.activity = game_activity

bot.version = '2.0'

bot.colors = lists.BOT_COLORS
bot.color_list = [c for c in bot.colors.values()]


def censoring(message, patterns):
    """
        Censors all cursed words in string
    """
    edited = message.lower()
    for pattern in patterns:
        if pattern in edited:
            regex_pattern = r"\b"+re.escape(pattern)+r"\b"
            edited = re.sub(regex_pattern, censor(pattern), edited)
        else:
            pass

    return edited


def censor(pattern):
    temp = pattern
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    # replacing the vowels with an ascii character.
    for char in temp:
        for v in vowels:
            if char == v:
                temp = temp.replace(char, '─')
    return temp


@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current activity:{bot.activity}\n-----")


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

    # Change to true if you want to enable censorship
    if lists.CENSORHIP_STATUS:
        try:
            msg = message.content
            channel = message.channel
            await bot.process_application_commands(message)
            """ 
            Without this coroutine, none of the commands will be triggered.
            """
            patterns = lists.CENSORED
            outcome = censoring(msg, patterns)
            # Check if message was censored then do something
            if "─" in outcome:
                await message.delete()
                await channel.send(message.author.mention + f" Censored: {outcome} ")
            else:
                pass

        except discord.errors.NotFound:
            return

        except discord.ext.commands.errors.CommandNotFound:
            return
    else:
        pass


@bot.slash_command(description="Ping-Pong game", guild_ids=[secrets.GUILD_ID])
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! {random.randrange(0, 1000)} ms")


@bot.slash_command(name='hi', aliases=['hello', 'yo'], description="Greets the user", guild_ids=[secrets.GUILD_ID])
async def _hi(ctx: discord.ApplicationContext):
    """
        A simple command which says hi to the author.
    """
    await ctx.respond(f"Hi {ctx.author.mention}!")


@bot.slash_command(description="Deletes the messages from channel", guild_ids=[secrets.GUILD_ID])
@commands.is_owner()
async def clear(
    ctx: discord.ApplicationContext,
    limit: Option(int, "Enter number of messages")
):
    """
        Deletes number of messages specified by user
    """
    await ctx.channel.purge(limit=limit)
    await ctx.respond("Channel cleared!")


@clear.error
async def clear_error(ctx: discord.ApplicationContext, error):
    """
        Error handler for cleaning function
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


@bot.slash_command(description="Turns off the bot", guild_ids=[secrets.GUILD_ID])
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


@bot.slash_command(description="Shows bot information", guild_ids=[secrets.GUILD_ID])
async def stats(ctx: discord.ApplicationContext):
    """
        A usefull command that displays bot statistics.
    """
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(bot.guilds)
    member_count = len(set(bot.get_all_members()))

    embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF',
                          colour=ctx.author.colour)

    embed.add_field(name='Python Version:', value=python_version)
    embed.add_field(name='Discord.Py Version', value=dpy_version)
    embed.add_field(name='Total Guilds:', value=server_count)
    embed.add_field(name='Total Users:', value=member_count)
    embed.add_field(name='Bot Developers:',
                    value="<@503505263119040522>,<@453579828281475084>")

    embed.set_footer(text=f"{bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)

    await ctx.respond(embed=embed)


@bot.slash_command(description="Sends information to specific channel.", guild_ids=[secrets.GUILD_ID])
async def source(
        ctx: discord.ApplicationContext,
        info: Option(str, "Enter your information"),
        chan: Option(discord.TextChannel, "Select a channel"),
        topic: Option(str, "Enter your title")
):
    temp = chan.name
    if temp not in lists.BLOCKED_CHANNELS:
        embed = discord.Embed(title=topic, description='\uFEFF',
                              colour=ctx.author.colour)
        embed.add_field(name="Information", value=info)
        guild = bot.get_guild(secrets.GUILD_ID)
        for channel in guild.channels:
            if channel.name == temp:
                await channel.send(embed=embed)
                await ctx.respond("Message sent!")
                return
        await ctx.respond("Channel not found!")
    else:
        await ctx.respond("You are not able to write messages in " + temp + " channel!")


@bot.slash_command(description="Prints all available channels", guild_ids=[secrets.GUILD_ID])
async def channels(ctx: discord.ApplicationContext):
    output = "**Channels list:**\n|"
    guild = bot.get_guild(secrets.GUILD_ID)
    for channel in guild.channels:
        if channel.name not in lists.BLOCKED_CHANNELS:
            output += channel.name+"|"
    await ctx.respond(output)


@bot.slash_command(name="help", description="Sends all available commands", guild_ids=[secrets.GUILD_ID])
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title=f'Available Commands:', description='\uFEFF',
                          colour=ctx.author.colour)
    for command in bot.application_commands:
        embed.add_field(name=f"{command}", value=command.description)
    await ctx.respond(embed=embed)


bot.run(secrets.OPEN_SOURCE_TOKEN)
