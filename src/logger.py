from datetime import datetime, date
from colorama import Fore

class Logger():
    def info(ctx):
        time = str(datetime.now()).split('.')[0]
        with open(f'./logs/{str(date.today())}.log', 'a', encoding = 'utf-8') as output_file:
            output_file.write(f'{time} {Fore.GREEN}INFO{Fore.RESET} {ctx}\n')
    def message(channel, author, ctx):
        time = str(datetime.now()).split('.')[0]
        with open(f'./logs/{str(date.today())}.log', 'a', encoding = 'utf-8') as output_file:
            output_file.write(f'{time} {Fore.CYAN}MESSAGE{Fore.RESET} {Fore.MAGENTA}[{channel}]{Fore.RESET} {author}: {ctx}\n')
