import discord
import random
import platform
import datetime
from logic.constants import BLOCKED_CHANNELS, CENSORHIP_STATUS, BOT_COLORS, ACTIVITIES
from logic.utilities import censor_message, RoleView
from protected import secrets
from types import SimpleNamespace
from discord.ext import commands
from discord.commands import Option


GUILD_ID = secrets.GUILD_ID
OPEN_SOURCE_TOKEN = secrets.OPEN_SOURCE_TOKEN


bot = commands.Bot(
    intents=discord.Intents.all(),
    status=discord.Status.streaming,
    activity=ACTIVITIES['STREAM']
)
bot.colors = BOT_COLORS
bot.color_list = SimpleNamespace(**bot.colors)


@bot.event
async def on_ready():
    channel = await bot.fetch_channel(936376047417569280)
    await channel.purge(limit=1)
    await channel.send("Will you share your knowledge with others and help all members of this server?", view=RoleView())
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current activity:{bot.activity}\n-----")


@bot.event
async def on_message(message: discord.Message):
    """
        Checks for users messages.
    """
    if message.author == (bot.user or message.author.bot):
        return
    # Change to true if you want to enable censorship
    if CENSORHIP_STATUS:
        channel = message.channel
        censored_message = censor_message(message.content)
        if message.content != censored_message:
            await message.delete()
            await channel.send(message.author.mention + f" Censored: {censored_message} ")


@bot.slash_command(description="Ping-Pong game.", guild_ids=[int(GUILD_ID)])
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! {random.randrange(0, 1000)} ms")


@bot.slash_command(description="Greets the user.", guild_ids=[int(GUILD_ID)])
async def hello(ctx: discord.ApplicationContext):
    """
        A simple command which says hi to the author.
    """
    await ctx.respond(f"Hi {ctx.author.mention}!")


@bot.slash_command(description="Tells user where is his/her dad.", guild_ids=[int(GUILD_ID)])
async def whereismydad(ctx: discord.ApplicationContext):
    """
        A simple command which says something to the author.
    """
    await ctx.respond(f"Went to buy milk for {ctx.author.mention}!")


@bot.slash_command(description="Deletes specified amount of messages from channel.", guild_ids=[int(GUILD_ID)])
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
    await ctx.channel.purge(limit=1)


@clear.error
async def clear_error(ctx: discord.ApplicationContext, error):
    """
        Error handler for cleaning function
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.slash_command(description="Turns off the bot.", guild_ids=[int(GUILD_ID)])
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
        await ctx.respond("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


@bot.slash_command(description="Shows bot information.", guild_ids=[int(GUILD_ID)])
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


@bot.slash_command(description="Sends information to specific channel in beautiful block.", guild_ids=[int(GUILD_ID)])
async def post(
        ctx: discord.ApplicationContext,
        info: Option(str, "Enter your information"),
        channel: Option(discord.TextChannel, "Select a channel"),
        topic: Option(str, "Enter your title")
):
    temp = channel.name
    if temp not in BLOCKED_CHANNELS:
        embed = discord.Embed(title=topic, description='\uFEFF',
                              colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Information", value=info)
        if (ctx.author.avatar == None):
            embed.set_footer(text=f"{ctx.author.name}",
                             icon_url=f"{bot.user.avatar.url}")
        else:
            embed.set_footer(text=f"{ctx.author.name}",
                             icon_url=f"{ctx.author.avatar.url}")
        guild = bot.get_guild(int(GUILD_ID))
        for ch in guild.channels:
            if ch.name == temp:
                await ch.send(embed=embed)
                await ctx.respond("Message sent!")
                await ctx.channel.purge(limit=1)
                return
        await ctx.respond("Channel not found!")
    else:
        await ctx.respond("You are not able to write messages in " + temp + " channel!")


@bot.slash_command(description="Shows all available channels for post command.", guild_ids=[int(GUILD_ID)])
async def channels(ctx: discord.ApplicationContext):
    guild = bot.get_guild(int(GUILD_ID))
    embed = discord.Embed(title=f'Available Channels:', description='\uFEFF',
                          colour=ctx.author.colour, timestamp=datetime.datetime.utcnow())
    for channel in guild.channels:
        if channel.name not in BLOCKED_CHANNELS:
            embed.add_field(name=f"{channel.name}:", value=channel.topic)
    embed.set_footer(text=f"{ctx.author.name}",
                     icon_url=f"{ctx.author.avatar.url}")
    await ctx.respond(embed=embed)


@bot.slash_command(description="Send files to specific channel.", guild_ids=[int(GUILD_ID)])
async def attach(
    ctx: discord.ApplicationContext,
    channel: Option(discord.TextChannel, "Select a channel"),
    attachment: discord.Attachment
):
    temp = channel.name
    if temp not in BLOCKED_CHANNELS:
        guild = bot.get_guild(int(GUILD_ID))
        tmp = await attachment.to_file(use_cached=False, spoiler=False)
        for ch in guild.channels:
            if ch.name == temp:
                await ch.send(f"**{tmp.filename}** sent by "+ctx.author.mention)
                await ch.send(file=tmp)
                await ctx.respond("File sent!")
                await ctx.channel.purge(limit=1)
                return
    else:
        await ctx.respond("You are not able to write messages in " + temp + " channel!")


@bot.slash_command(description="Shows all available commands.", guild_ids=[int(GUILD_ID)])
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


def activate():
    bot.run(OPEN_SOURCE_TOKEN)
