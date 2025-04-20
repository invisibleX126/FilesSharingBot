import asyncio

from pyrogram import filters, Client

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram.errors import FloodWait

from bot import Bot

from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON

from helper_func import encode




@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))

# Define an asynchronous function called channel_post that takes in a client and a message as parameters

async def channel_post(client: Client, message: Message):

    # Reply to the message with a "Please Wait..." text

    reply_text = await message.reply_text("Please Wait...!", quote = True)

    # Try to copy the message to the client's database channel
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)

    # If a FloodWait exception is raised, sleep for the duration of the exception

    except FloodWait as e:

        await asyncio.sleep(e.x)

        # Try to copy the message to the client's database channel again

        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)

    # If any other exception is raised, print the exception and edit the reply text to "Something Went Wrong..!"

    except Exception as e:

        print(e)

        await reply_text.edit_text("Something Went Wrong..!")

        return
    
    # Calculate the converted ID of the post message

    converted_id = post_message.id * abs(client.db_channel.id)

    # Create a string with the converted ID

    string = f"get-{converted_id}"

    # Encode the string into a base64 string

    base64_string = await encode(string)

    # Create a link with the base64 string

    link = f"https://t.me/{client.username}?start={base64_string}"


    # Create an inline keyboard markup with a button to share the link

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Edit the reply text to include the link and the inline keyboard markup

    await reply_text.edit(f"<b>Here Is Your Link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    # If the DISABLE_CHANNEL_BUTTON variable is not set to True, edit the post message to include the inline keyboard markup
    if not DISABLE_CHANNEL_BUTTON:

        await post_message.edit_reply_markup(reply_markup)





@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))

# Define an asynchronous function called new_post that takes in a Client and Message object as parameters

async def new_post(client: Client, message: Message):

    # Check if the DISABLE_CHANNEL_BUTTON variable is set to True

    if DISABLE_CHANNEL_BUTTON:

        # If it is, return and do nothing

        return

    # Convert the message id and the client db_channel id to a string

    converted_id = message.id * abs(client.db_channel.id)

    # Create a string that starts with "get-" and is followed by the converted id

    string = f"get-{converted_id}"

    # Encode the string using the encode function

    base64_string = await encode(string)

    # Create a link that starts with "https://t.me/" followed by the client username and "?start=" followed by the base64 string

    link = f"https://t.me/{client.username}?start={base64_string}"

    # Create an InlineKeyboardMarkup object with a button that says "🔁 Share URL" and links to the link

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Try to edit the reply_markup of the message

    try:

        await message.edit_reply_markup(reply_markup)

    # If an exception is raised, print the exception and pass

    except Exception as e:

        print(e)
        
        pass






# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
