from discord import Intents, Message, Status, DMChannel
from discord.ext.commands import Bot, Context
from logger import Logger
from config import Config
from random import randint

class Multitasker(Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.add_commands()

    def add_commands(self):
        # Send anonymous messages
        @self.command(name = 'say')
        async def say(ctx: Context):
            temp = ctx.message.content.split(' ')
            await ctx.message.delete()
            if len(temp) > 1:
                anonymous_message = ' '.join(temp[1:])
                await ctx.send(f'{anonymous_message}')
            else:
                await ctx.send('Say what?')

        @self.command(name = 'purgedm')
        async def purgedm(ctx: Context):
            await ctx.author.create_dm()
            async for message in ctx.author.dm_channel.history(limit = None):
                if message.author == bot.user: await message.delete()

        @self.command(name = 'purge')
        async def purge(ctx: Context):
            # await self.change_presence(status = Status.do_not_disturb)
            if ctx.message.author.name == admin:
                temp = ctx.message.content.split(' ')
                if len(temp) == 2:
                    try:
                        limit = int(temp[1])
                        await ctx.channel.purge(limit = limit + 1)
                        await ctx.send(f'Successfully deleted {limit} messages')
                    except:
                        await ctx.send('This command takes needs an integer as a argument')
                else:
                    await ctx.send('This command takes exactly one argument')
            else:
                await ctx.send('You don\'t have permission to use this command')
            # await self.change_presence(status = Status.online)

    async def on_message(self, message: Message):
        if isinstance(message.channel, DMChannel):
            if message.author == bot.user: return
            else: await message.channel.send('Send message on the server channel')
        else:
            Logger.message(message.channel, message.author.display_name, message.content)
            if message.author == bot.user: return
            else:
                await self.process_commands(message)

    async def on_ready(self):
        await self.change_presence(status = Status.online)
        Logger.info(f'Bot is now online and ready to serve')

# Config variables
prefix = Config().getPrefix()
token = Config().getToken()
admin = Config().getAdmin()
base_role = Config().getBaseRole()

# Instantiate the bot
bot = Multitasker(command_prefix = prefix, intents = Intents.all())

# Run the bot with your token
bot.run(token, log_handler = None)