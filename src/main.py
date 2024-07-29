from discord import ButtonStyle, Intents, Interaction, Message, SelectOption, Status, DMChannel, Embed
from discord.ext.commands import Bot, Context
from discord.ui import View, Select, Button
from logger import Logger
from config import Config
from os import listdir, remove

# class DropdownSelectView(View):
#     def __init__(self):
#         super().__init__()
#         # Add a dropdown menu with options
#         self.add_item(Dropdown())
#         # Add a submit button
#         self.add_item(SubmitButton())

# class Dropdown(Select):
#     def __init__(self):
#         options = [
#             SelectOption(label="Option 1", description="This is the first option", value="1"),
#             SelectOption(label="Option 2", description="This is the second option", value="2"),
#             SelectOption(label="Option 3", description="This is the third option", value="3")
#         ]
#         super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)
#         self.selected_value = None  # To store the selected value

#     async def callback(self, interaction: Interaction):
#         self.selected_value = self.values[0]
#         # Optionally, you can send a message indicating the selection
#         await interaction.response.send_message(f"Option selected: {self.selected_value}", ephemeral=True)

# class SubmitButton(Button):
#     def __init__(self):
#         super().__init__(label="Submit", style=ButtonStyle.primary)

#     async def callback(self, interaction: Interaction):
#         dropdown: Dropdown = next(item for item in self.view.children if isinstance(item, Dropdown))
#         if dropdown.selected_value:
#             await interaction.response.send_message(f"You submitted: {dropdown.selected_value}")
#         else:
#             await interaction.response.send_message("Please select an option first.", ephemeral=True)

class Multitasker(Bot):
    # Initialize bot object
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix = command_prefix, intents = intents)
        self.add_commands()
    # Register bot commands
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
        # Manage counters for various user defined features
        @self.command(name = 'counter')
        async def counter(ctx: Context):
            temp = ctx.message.content.split(' ')
            path = './data/counters'
            await ctx.message.delete()
            try:
                if temp[1] == 'list':
                    response = ''
                    for file in listdir(path):
                        response += f'{file}  '
                    if response != '':
                        await ctx.send(f'Existing counters: {response}')
                    else:
                        await ctx.send(f'No counters available')
                elif temp[1] == 'create':
                    for file in listdir(path):
                        if file == temp[2]:
                            await ctx.send('Counter already exist')
                            return
                    counter = open(f'./data/counters/{temp[2]}', 'w')
                    counter.close()
                    await ctx.send(f'Counter created')
                elif temp[1] == 'delete':
                    if ctx.author.id == admin:
                        for file in listdir(path):
                            if file == temp[2]:
                                remove(f'./data/counters/{temp[2]}')
                                await ctx.send('Counter deleted')
                                return
                        await ctx.send('Such counter does not exist')
                    else:
                        await ctx.send('You need permission to use this command')
                elif temp[1] == '++':
                    flag = False
                    for file in listdir(path):
                        if file == temp[2]:
                            counter = open(f'./data/counters/{file}', 'r')
                            lines = counter.readlines()
                            counter.close()
                            counter = open(f'./data/counters/{file}', 'w')
                            for line in lines:
                                if temp[3] in line:
                                    line = f"{line.split(' ')[0]} {int(line.split(' ')[1]) + 1}\n"
                                    flag = True
                                counter.write(line)
                            if flag == False:
                                counter.write(f'{temp[3]} 1\n')
                            counter.close()
                            await ctx.send('Counter incremented')
                            return
                    await ctx.send('Such counter does not exist')
            except:
                await ctx.send('Incorrect syntax!')
            # embed = Embed(title="Select an Option", description="Please choose an option from the dropdown menu below and click Submit.")
            # view = DropdownSelectView()
            # await ctx.send(embed = embed, view = view)
        # Clear messages within DM channel
        @self.command(name = 'purgedm')
        async def purgedm(ctx: Context):
            await ctx.author.create_dm()
            async for message in ctx.author.dm_channel.history(limit = None):
                if message.author == bot.user: await message.delete()
        # Clear messages within text channel (admin only)
        @self.command(name = 'purge')
        async def purge(ctx: Context):
            if ctx.message.author.id == admin:
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
    # Handler for every incoming server message
    async def on_message(self, message: Message):
        if isinstance(message.channel, DMChannel):
            if message.author == bot.user: return
            else: await message.channel.send('Send message on the server channel')
        else:
            Logger.message(message.channel, message.author.display_name, message.content)
            if message.author == bot.user: return
            else:
                await self.process_commands(message)
    # Runs every time bot is being initialized
    async def on_ready(self):
        await self.change_presence(status = Status.online)
        Logger.info(f'Bot is now online and ready to serve')
# Config variables
prefix = Config().getPrefix()
token = Config().getToken()
admin = (int) (Config().getAdmin())
base_role = Config().getBaseRole()
# Instantiate the bot
bot = Multitasker(command_prefix = prefix, intents = Intents.all())
# Run the bot with your token
bot.run(token, log_handler = None)