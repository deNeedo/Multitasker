from datetime import datetime, date
from colorama import Fore

# # Define the file where you want to redirect stdout
file_name = f'./logs/{str(date.today())}.log'

class Logger():
    def info(ctx):
        time = str(datetime.now()).split('.')[0]
        with open(file_name, 'a', encoding = 'utf-8') as output_file:
            output_file.write(f'{time} {Fore.GREEN}INFO{Fore.RESET} {ctx}\n')
    def message(channel, author, ctx):
        time = str(datetime.now()).split('.')[0]
        with open(file_name, 'a', encoding = 'utf-8') as output_file:
            output_file.write(f'{time} {Fore.CYAN}MESSAGE{Fore.RESET} {Fore.MAGENTA}[{channel}]{Fore.RESET} {author}: {ctx}\n')
