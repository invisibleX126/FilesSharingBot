from pyrogram import __version__

from bot import Bot

from config import OWNER_ID

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery



@Bot.on_callback_query()

# Define an asynchronous function called cb_handler that takes in a Bot object and a CallbackQuery object as parameters

async def cb_handler(client: Bot, query: CallbackQuery):

    # Get the data from the CallbackQuery object

    data = query.data

    # If the data is "about", edit the message with the following text

    if data == "about":                 # Change

        await query.message.edit_text(

            text = f"<b>🤖 My Name :</b> <a href='https://t.me/FileSharingXProBot'>File Sharing Bot</a> \n<b>📝 Language :</b> <a href='https://python.org'>Python 3</a> \n<b>📚 Library :</b> <a href='https://pyrogram.org'>Pyrogram {__version__}</a> \n<b>🚀 Server :</b> <a href='https://heroku.com'>Heroku</a> \n<b>📢 Channel :</b> <a href='https://t.me/Madflix_Bots'>Madflix Botz</a> \n<b>🧑‍💻 Developer :</b> <a href='tg://user?id={OWNER_ID}'>Jishu Developer</a>",

            disable_web_page_preview = True,

            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )

    # If the data is "close", delete the message and the message it was replying to

    elif data == "close":

        await query.message.delete()

        try:

            await query.message.reply_to_message.delete()

        except:
            
            pass





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
