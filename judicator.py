import discord
import secrets
import random
from discord.ext import commands
import platform  # For stats

intents = discord.Intents.all()

"""Different bot activities"""
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

bot.version = '1'

bot.colors = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

# List of blocked channels for source & channels commands
blocked_channels = {
    'Text', 'Voice Channels', 'soulstorm-mods',
    'Room1', 'Room2', 'Warhammer Archives', 'файло-помойка',
    'AFK', 'system', 'Solutions & Suggestions', 'suggestions',
    'exercise-discussions', 'thanks-ivan-kuzmin', 'shortcuts',
    'memes', 'ca-homework', 'trash-can', 'welcome', 'mod_channel',
    'fop-solutions', 'ca-solutions', 'ds-solutions', 'main'
}


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


@bot.command(description="Ping-Pong game")
async def ping(ctx: commands.Context):
    await ctx.send("Pong! {0} ms".format(random.randrange(0, 1000)))


@bot.command(name='hi', aliases=['hello', 'yo'], description="Greets the user")
async def _hi(ctx):
    """
    A simple command which says hi to the author.
    """
    await ctx.send(f"Hi {ctx.author.mention}!")


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

    #embed.add_field(name='Bot Version:', value=bot.version)
    embed.add_field(name='Python Version:', value=python_version)
    embed.add_field(name='Discord.Py Version', value=dpy_version)
    embed.add_field(name='Total Guilds:', value=server_count)
    embed.add_field(name='Total Users:', value=member_count)
    embed.add_field(name='Bot Developers:',
                    value="<@503505263119040522>,<@453579828281475084>")

    embed.set_footer(text=f"{bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name='vc', aliases=['voicechat'], description="Sends voice channel")
async def vc(ctx):
    """
    A simple command which says hi to the author.
    """
    await ctx.send("<#636965781208432651>")


@bot.command(description="Send information to specific channel.\nTakes 3 arguments: information,channel,title (always wrap in quotation marks)")
async def source(ctx: commands.Context, info, chan, topic):
    if chan not in blocked_channels:
        embed = discord.Embed(title=topic, description='\uFEFF',
                              colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.add_field(name="Information", value=info)
        guild = bot.get_guild(636962982286589952)
        for channel in guild.channels:
            if channel.name == chan:
                await channel.send(embed=embed)
                return
        await ctx.send("Channel not found!")
    else:
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
        if channel.name not in blocked_channels:
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
