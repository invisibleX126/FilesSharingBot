from pyrogram import filters, enums

from pyrogram.types import Message

from bot import Bot




@Bot.on_message(filters.command("id") & filters.private)

# Define an asynchronous function called showid that takes in a client and a message as parameters

async def showid(client, message):

    # Get the type of chat the message is from

    chat_type = message.chat.type


    # If the chat type is private

    if chat_type == enums.ChatType.PRIVATE:

        # Get the user ID of the chat

        user_id = message.chat.id

        # Reply to the message with the user ID

        await message.reply_text(

            f"<b>Your User ID Is :</b> <code>{user_id}</code>", 
            
            quote=True
        )
        





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
