import discord, configparser
from discord.ext import commands

config = configparser.ConfigParser()
config.read('./config.env')
admin = config.get('sys','admin')
base_role = config.get('sys','base_role')
prefix = config.get('bot','prefix')
token = config.get('bot','token')
config.get('sys','base_role')


intents = discord.Intents.all()

bot = commands.Bot(command_prefix = prefix, intents = intents, help_command = None)

@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help"))
    print(f"{bot.user} is now online!")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name = base_role)
    await member.add_roles(role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if message.content.startswith(f'{prefix}purge '):
            if str(message.author) == str(admin):
                args = message.content.split(' ')
                try:
                    limit = int(args[1])
                    while limit > 0:
                        await message.channel.purge(limit = 1)
                        limit -= 1
                except:
                    await message.channel.send(content = 'Something went wrong!')
            else:
                await message.channel.send(content = 'You don\'t have permission to use this command!')

bot.run(token)