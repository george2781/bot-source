import discord
from discord.ext import commands
from discord.utils import get
import os
import random
from discord.ext.commands import has_permissions, MissingPermissions



intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
#intents = discord.Intents(
#    guilds=True,
#    members=True,
#    messages=True,
#)


client = commands.Bot(intents=intents, command_prefix='>', help_command=None)



@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed(title="Hello there!", color=discord.Color.dark_purple())
            embed.add_field(name="Introduction message", value="Hello! This bot has been added to your server successfully! To get started with this bot, execute >help (just type it, no slash command bullshit). This message will delete itself after 1 minute.", inline=False)
            embed.set_footer(text="Report bugs to george2781#2781")
            await channel.send(embed=embed, delete_after=60)
        break


@client.event
async def on_ready():
    print("login SUCCESS! Logged in as: " + client.user.name + "\n")
    print('BOT user is now ACTIVE, please maintain if possible')
    await client.change_presence(
        activity=discord.Streaming(name="I'm back (I guess)", url='https://github.com/george2781/bot-source',
                                   activity="EOL bot returns"))
    print("Guilds this bot is in")
    for guild in client.guilds:
        print(guild.name, guild.id)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title=":x: Ok do that again but actually put the requirements there.", color=discord.Color.dark_purple())
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title=":x: Missing permissions", color=discord.Color.dark_purple())
        await ctx.send(embed=embed)
    if isinstance(error, commands.NotOwner):
        embed=discord.Embed(title=":x: Owner only command", color=discord.Color.dark_purple())
        await ctx.send(embed=embed)



@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left/been kicked/banned from a server')



@client.command()
async def ping(ctx):
    await ctx.send(f'Latency is {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'No.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    responses = random.choice(responses)
    embed=discord.Embed(title="8ball", description="Ask the 8ball!", color=discord.Color.dark_purple())
    embed.add_field(name="Q: " + question, value="A:" + responses, inline=False)
    await ctx.send(embed=embed)


@client.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='N/A'):
    await member.kick(reason=reason)
    embed=discord.Embed(title="Kick tool", color=discord.Color.dark_purple())
    embed.add_field(name=f"Kicking of {member}", value=f"Successfully kicked target for {reason}!", inline=False)
    embed.set_footer(text="Beta function, expect bugs!")
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='N/A'):
    await member.ban(reason=reason) 
    embed=discord.Embed(title="Ban tool", color=discord.Color.dark_purple())
    embed.add_field(name=f"Banning of {member}", value=f"Successfully banned target for {reason}!", inline=False)
    embed.set_footer(text="Beta function, expect bugs!")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member, ):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed=discord.Embed(title="Unban tool", color=discord.Color.dark_purple())
            embed.add_field(name=f"Unbanning of {user}", value=f"Successfully unbanned target!", inline=False)
            embed.set_footer(text="Beta function, expect bugs!")
            await ctx.send(embed=embed)
            return


@client.command()
async def help(ctx):
    embed = discord.Embed(title="George's testing bot",
                          description="This is the help command, it will show all available commands",
                          colour=discord.Color.dark_purple())
    embed.add_field(name="help", value="This command!")
    embed.add_field(name="8ball", value="Ask the 8ball")
    embed.add_field(name="kick", value="Kicks someone, kick perms are needed ofc")
    embed.add_field(name="ban", value="Bans someone, ban perms are needed ofc")
    embed.add_field(name="unban", value="Unbans someone, ban perms are needed ofc")
    embed.add_field(name="ping", value="Gets bot latency")
    embed.add_field(name="clear", value="Clears messages, default is 10")
    embed.add_field(name="invite", value="Gives you the bot's invite link")
    embed.add_field(name="faq", value="Shows the FAQ prompt.")
    embed.add_field(name="source", value="Shows the source code.")
    embed.add_field(name="userinfo", value="Displays information about a user (or yourself)")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_footer(text="WARNING: This bot is discontinued-ish, see >faq")

    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.send(
        f'You can no longer invite this bot to new servers, ask me to add it to your server if you want.')


@client.command()
async def faq(ctx):
    embed=discord.Embed(title="FAQ", description="Frequently Asked Questions", color=discord.Color.dark_purple())
    embed.add_field(name="Q: Where is the alpha version of the bot", value="That version of the bot is private.", inline=False)
    embed.add_field(name="Q: How do you host 2 bots?", value="One is hosted on heroku, the other is stored locally.", inline=False)
    embed.add_field(name="Q: Who are you?", value="To be honest I don't really know myself.", inline=False)
    embed.add_field(name="Q: Can you help me learn to code", value="No.", inline=False)
    embed.add_field(name="Q: What motivates you to host the bot", value="Mostly a feeling of satisfaction for coding the bot, this isn't easy to pick up for most people yet I managed to do it anyway, it gives me a sense of fulfilment really.", inline=False)
    embed.add_field(name="Q: Why make an FAQ command?", value="So you don't ask me repetetive questions 🙃", inline=False)
    embed.add_field(name="Q: Isn't this bot dead?", value="Short answer: Yesn't. I revived the bot because its functions were useful to me, therefore the bot is being 'privated' I guess, only servers I want to have the bot in or those with it already in will have access to it and it's functions. I wouldn't call this a 'revival' really but there's no other short way to describe it.", inline=False)
    embed.set_footer(text="Now stop asking me")
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

   
@client.command()
async def source(ctx):
    embed=discord.Embed(title="Source code", description="https://github.com/george2781/bot-source/tree/main", color=discord.Color.dark_purple())
    embed.set_footer(text="Open source ftw")
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, *, user: discord.Member = None):
    if isinstance(ctx.channel, discord.DMChannel):
        return
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=discord.Color.dark_purple(), description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    await ctx.send(embed=embed)
    
@client.command()
async def showguilds(ctx):
    embed = discord.Embed(color=discord.Color.dark_purple(), description="Guilds with this bot in them.")
    for guild in client.guilds:
#        message += f"{guild.name}\n"
        embed.add_field(name=f"{guild.name}\n", value=str(guild.id), inline=False)
    await ctx.send(embed=embed)
    
client.run('token')
