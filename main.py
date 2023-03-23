import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv
import logging.handlers
from pretty_help import PrettyHelp

load_dotenv()

GUILD = os.getenv('DISCORD_GUILD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
hello_channel = int(os.getenv('hello_channel'))
basic_role = int(os.getenv('basic_role'))

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=PrettyHelp())


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    # В какой канал будет отправляться приветствие
    channel = bot.get_channel(hello_channel)
    await channel.send(
        f'Привет {member.name}, Добро Пожаловать на наш сервер!'
    )
    role = guild.get_role(basic_role)
    if role is None:
        # Убедитесь, что роль все еще существует и является действительной.
        return
    await member.add_roles(role)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Недостаточно прав для команды.')


@bot.command(name='my-role', help='Дает тебе роль на сервере, если у тебя есть необходимые на нее права')
@commands.has_role('admin')
async def my_role(ctx, name_role: str):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    roles = guild.roles
    role = list(filter(lambda x: x.name == name_role, roles))
    await ctx.author.add_roles(*role)


@bot.command(name='create-channel', help='Создает текстовый канал с указанным названием')
@commands.has_role('admin')
async def create_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='roll', help='Бросает 6-гранный кубик n-раз"')
async def roll(ctx, number_of_dice: int):
    dice_of_sides = {
        1: ':one:',
        2: ':two:',
        3: ':three:',
        4: ':four:',
        5: ':five:',
        6: ':six:'
    }
    roll_dice = [dice_of_sides.get((random.choice(range(1, 7))))
                 for _ in range(number_of_dice)]
    await ctx.send('      '.join(roll_dice))

bot.run(BOT_TOKEN, log_handler=None)