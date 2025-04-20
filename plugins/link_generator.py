from pyrogram import Client, filters

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import Bot

from config import ADMINS

from helper_func import encode, get_message_id



@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))

async def batch(client: Client, message: Message):

    # Loop until a valid first message is received

    while True:

        try:

            # Ask the user to forward the first message from the DB channel

            first_message = await client.ask(text = "Forward The First Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)

        except:

            # If an exception is raised, return

            return
        
        # Get the message ID of the first message

        f_msg_id = await get_message_id(client, first_message)

        # If a valid message ID is received, break the loop

        if f_msg_id:

            break

        else:
            # If an invalid message ID is received, reply with an error message

            await first_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)

            continue

    # Loop until a valid second message is received

    while True:

        try:

            # Ask the user to forward the last message from the DB channel

            second_message = await client.ask(text = "Forward The Last Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)

        except:

            # If an exception is raised, return

            return
        
        # Get the message ID of the second message

        s_msg_id = await get_message_id(client, second_message)

        # If a valid message ID is received, break the loop

        if s_msg_id:

            break

        else:

            # If an invalid message ID is received, reply with an error message

            await second_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)

            continue


    # Create a string with the message IDs and the DB channel ID

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"

    # Encode the string to base64

    base64_string = await encode(string)

    # Create a link with the encoded string

    link = f"https://t.me/{client.username}?start={base64_string}"

    # Create a reply markup with a button to share the link

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Reply with the link and the share button

    await second_message.reply_text(f"<b>Here Is Your Link</b>\n\n{link}", quote=True, reply_markup=reply_markup)




@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))

# Define an asynchronous function called link_generator that takes in a Client and Message object as parameters

async def link_generator(client: Client, message: Message):

    # Create an infinite loop

    while True:

        # Try to get a message from the user

        try:

            # Ask the user to forward a message from the DB channel or send the DB channel post link

            channel_message = await client.ask(text = "Forward Message From The DB Channel (With Quotes)..\n\nOr Send The DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)

        # If an error occurs, return

        except:

            return
        
        # Get the message ID from the forwarded message

        msg_id = await get_message_id(client, channel_message)

        # If the message ID is valid, break the loop

        if msg_id:

            break

        # Otherwise, reply to the user with an error message

        else:

            await channel_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)

            continue

    # Encode the message ID and the DB channel ID into a base64 string

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")

    # Create a link using the base64 string

    link = f"https://t.me/{client.username}?start={base64_string}"

    # Create a reply markup with a button to share the link

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    
    # Reply to the user with the link and the reply markup

    await channel_message.reply_text(f"<b>Here Is Your Link</b>\n\n{link}", quote=True, reply_markup=reply_markup)







# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
