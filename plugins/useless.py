from bot import Bot

from pyrogram.types import Message

from pyrogram import filters

from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT

from datetime import datetime

from helper_func import get_readable_time




@Bot.on_message(filters.command('stats') & filters.user(ADMINS))

# Define an asynchronous function called stats that takes in a bot and a message as parameters

async def stats(bot: Bot, message: Message):

    # Get the current date and time

    now = datetime.now()

    # Calculate the time difference between the current date and time and the bot's uptime

    delta = now - bot.uptime

    # Convert the time difference to a readable format

    time = get_readable_time(delta.seconds)

    # Reply to the message with the bot's stats

    await message.reply(BOT_STATS_TEXT.format(uptime=time))



@Bot.on_message(filters.private & filters.incoming)

# Define an asynchronous function called 'useless' that takes two parameters, '_' and 'message'

async def useless(_,message: Message):

    # Check if the 'USER_REPLY_TEXT' variable is set

    if USER_REPLY_TEXT:

        # If it is, reply to the message with the 'USER_REPLY_TEXT' variable
        
        await message.reply(USER_REPLY_TEXT)





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
