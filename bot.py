import discord
from discord.ext import commands
from discord.utils import get
import os
import random
from discord.ext.commands import has_permissions, MissingPermissions

client = commands.Bot(command_prefix='>', help_command=None)


@client.event
async def on_ready():
    print("login SUCCESS! Logged in as: " + client.user.name + "\n")
    print('BOT user is now ACTIVE, please maintain if possible')
    await client.change_presence(
        activity=discord.Streaming(name="Check out Loki!", url='https://www.twitch.tv/lokiicedcoffee',
                                   activity="Check out My friend Loki's streams!"))


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
    embed.add_field(name="eol", value="Why the bot is currently EOL")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_footer(text="WARNING: This bot is discontinued, for more info execute >eol")

    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.send(
        f'To invite the bot to a server, click the link here: https://discord.com/api/oauth2/authorize?client_id=743119025575428206&permissions=8&scope=bot')


@client.command()
async def faq(ctx):
    embed=discord.Embed(title="FAQ", description="Frequently Asked Questions", color=discord.Color.dark_purple())
    embed.add_field(name="Q: Where is the alpha version of the bot", value="That version of the bot is private.", inline=False)
    embed.add_field(name="Q: How do you host 2 bots?", value="One is hosted on heroku, the other is stored locally.", inline=False)
    embed.add_field(name="Q: Who are you?", value="To be honest I don't really know myself.", inline=False)
    embed.add_field(name="Q: Can you help me learn to code", value="No.", inline=False)
    embed.add_field(name="Q: What motivates you to host the bot", value="Mostly a feeling of satisfaction for coding the bot, this isn't easy to pick up for most people yet I managed to do it anyway, it gives me a sense of fulfilment really.", inline=False)
    embed.add_field(name="Q: Why make an FAQ command?", value="So you don't ask me repetetive questions 🙃", inline=False)
    embed.set_footer(text="Now stop asking me")
    await ctx.send(embed=embed)


@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command()
async def eol(ctx):
    embed=discord.Embed(title="End of life", description="This bot is discontinued.", color=discord.Color.dark_purple())
    embed.add_field(name="Indeed, I am ending this project", value="It was fun to run this bot, however discord is changing and in the near future I won't be able to properly develop this bot anymore. This is mostly due to the discontinuation of Discord.py, which was caused by slash commands becoming the ONLY type of command feasible to use. I suggest looking at the document that the discord.py dev made linked here. https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1", inline=False)
    embed.add_field(name="So this is goodbye?", value="Sadly, yes. Without a proper up-to-date library I don't have any way to code for this bot without radically changing the code, let alone the mandation of slash commands by April 2022.", inline=False)
    embed.add_field(name="What does this mean for me?", value="For anyone who isn't a developer these changes will be trivial to you, for anyone else who doesn't use slash commands it'll mean you have to use them by April 2022 and for amyone else using discord.py as their library it'll mean you have to find a new one.", inline=False)
    embed.add_field(name="Will you open source the bot/let me continue the bot?", value="I'll be open sourcing the bot to a command called 'source', when that command is released you are free to use it however you like.", inline=False)
    embed.add_field(name="What now?", value="This marks the end of me developing this bot, it will continue to run until April 2022 when it will eventually crash. I will not revive this project.", inline=False)
    embed.set_footer(text="It really is the end.")
    await ctx.send(embed=embed)
   
@client.command()
async def source(ctx):
    embed=discord.Embed(title="Source code", description="https://github.com/george2781/bot-source/tree/main", color=discord.Color.dark_purple())
    embed.set_footer(text="It really is the end.")
    await ctx.send(embed=embed)

    
    
client.run('bot token goes here')
