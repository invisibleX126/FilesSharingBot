import os, asyncio, humanize

from pyrogram import Client, filters, __version__

from pyrogram.enums import ParseMode

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot

from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE

from helper_func import subscribed, encode, decode, get_messages

from database.database import add_user, del_user, full_userbase, present_user

# Define a variable madflixofficials and assign it the value of FILE_AUTO_DELETE

madflixofficials = FILE_AUTO_DELETE

# Define a variable jishudeveloper and assign it the value of madflixofficials

jishudeveloper = madflixofficials

# Define a variable file_auto_delete and assign it the value of humanize.naturaldelta(jishudeveloper)

file_auto_delete = humanize.naturaldelta(jishudeveloper)





@Bot.on_message(filters.command('start') & filters.private & subscribed)

async def start_command(client: Client, message: Message):

    # Get the user id from the message

    id = message.from_user.id

    # Check if the user is present in the database

    if not await present_user(id):

        # If not, try to add the user to the database

        try:

            await add_user(id)

        except:

            # If there is an error, pass

            pass

    # Get the text from the message

    text = message.text

    # If the text is longer than 7 characters

    if len(text)>7:

        # Try to split the text into a base64 string

        try:

            base64_string = text.split(" ", 1)[1]

        except:

            # If there is an error, return

            return
        
        # Decode the base64 string

        string = await decode(base64_string)

        # Split the decoded string into an argument

        argument = string.split("-")

        # If the argument has 3 elements

        if len(argument) == 3:

            # Try to convert the second and third elements to integers

            try:

                start = int(int(argument[1]) / abs(client.db_channel.id))

                end = int(int(argument[2]) / abs(client.db_channel.id))

            except:

                # If there is an error, return

                return
            
            # If the start is less than or equal to the end

            if start <= end:

                # Create a range from start to end

                ids = range(start,end+1)

            else:

                # If the start is greater than the end, create an empty list

                ids = []

                # Create a while loop to append the start to the list

                i = start

                while True:

                    ids.append(i)

                    i -= 1

                    # If the start is less than the end, break the loop

                    if i < end:

                        break

        # If the argument has 2 elements

        elif len(argument) == 2:

            # Try to convert the second element to an integer

            try:

                ids = [int(int(argument[1]) / abs(client.db_channel.id))]

            except:

                # If there is an error, return

                return
            
        # Create a temporary message to show the user that the process is ongoing

        temp_msg = await message.reply("Please Wait...")

        # Try to get the messages from the database

        try:

            messages = await get_messages(client, ids)

        except:

            # If there is an error, send a message to the user

            await message.reply_text("Something Went Wrong..!")

            return
        
        # Delete the temporary message

        await temp_msg.delete()

    
        madflix_msgs = [] # List to keep track of sent messages

        for msg in messages:

            # Check if CUSTOM_CAPTION is set and if the message has a document

            if bool(CUSTOM_CAPTION) & bool(msg.document):

                # Format the CUSTOM_CAPTION with the previous caption and filename

                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)

            else:

                # If CUSTOM_CAPTION is not set or the message does not have a document, use the caption from the message

                caption = "" if not msg.caption else msg.caption.html

            # Check if DISABLE_CHANNEL_BUTTON is set

            if DISABLE_CHANNEL_BUTTON:

                # If set, use the reply_markup from the message

                reply_markup = msg.reply_markup

            else:

                # If not set, set reply_markup to None

                reply_markup = None


            try:

                # Copy the message to the user's chat with the caption and reply_markup

                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)

                # await asyncio.sleep(0.5)

                # Add the copied message to the madflix_msgs list

                madflix_msgs.append(madflix_msg)

                
            except FloodWait as e:

                # If a FloodWait exception is raised, sleep for the duration of the exception

                await asyncio.sleep(e.x)

                # Copy the message to the user's chat with the caption and reply_markup

                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)

                # Add the copied message to the madflix_msgs list

                madflix_msgs.append(madflix_msg)
                
            except:

                # If any other exception is raised, pass

                pass


        k = await client.send_message(chat_id = message.from_user.id, text=f"<b>❗️ <u>IMPORTANT</u> ❗️</b>\n\nThis Video / File Will Be Deleted In {file_auto_delete} (Due To Copyright Issues).\n\n📌 Please Forward This Video / File To Somewhere Else And Start Downloading There.")

        # Schedule the file deletion

        asyncio.create_task(delete_files(madflix_msgs, client, k))

        
        # for madflix_msg in madflix_msgs: 

            # try:

                # await madflix_msg.delete()

                # await k.edit_text("Your Video / File Is Successfully Deleted ✅") 

            # except:    

                # pass 

        return
    
    else:

        # Create an inline keyboard markup with two buttons

        reply_markup = InlineKeyboardMarkup(

            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),

                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )

        # Send a message to the user with their first name, last name, username, mention, and id

        await message.reply_text(

            text = START_MSG.format(

                first = message.from_user.first_name,

                last = message.from_user.last_name,

                username = None if not message.from_user.username else '@' + message.from_user.username,

                mention = message.from_user.mention,

                id = message.from_user.id
            ),

            reply_markup = reply_markup,

            disable_web_page_preview = True,

            quote = True

        )

        return

    



    
    
@Bot.on_message(filters.command('start') & filters.private)

# Define an asynchronous function called not_joined that takes in a client and a message as parameters

async def not_joined(client: Client, message: Message):

    # Create a list of buttons with a single button that links to the client's invite link

    buttons = [

        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink)
        ]
    ]
    # Try to append another button to the list that links to the client's username with a start command

    try:

        buttons.append(

            [
                InlineKeyboardButton(

                    text = 'Try Again',

                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    # If the index is out of range, pass

    except IndexError:

        pass

    # Reply to the message with a formatted text message and the buttons, quote the message, and disable web page preview

    await message.reply(

        text = FORCE_MSG.format(

                first = message.from_user.first_name,

                last = message.from_user.last_name,

                username = None if not message.from_user.username else '@' + message.from_user.username,

                mention = message.from_user.mention,

                id = message.from_user.id

            ),

        reply_markup = InlineKeyboardMarkup(buttons),

        quote = True,

        disable_web_page_preview = True
    )



@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))

# Define an asynchronous function called get_users that takes in a client and a message as parameters

async def get_users(client: Bot, message: Message):

    # Send a message to the chat_id of the message with the text "Processing..."

    msg = await client.send_message(chat_id=message.chat.id, text=f"Processing...")

    # Call the full_userbase function and store the result in the users variable

    users = await full_userbase()

    # Edit the message sent earlier with the text showing the number of users using the bot

    await msg.edit(f"{len(users)} Users Are Using This Bot")



@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))

async def send_text(client: Bot, message: Message):

    # Check if the message is a reply to another message

    if message.reply_to_message:

        # Get the full userbase

        query = await full_userbase()

        # Get the message to be broadcasted

        broadcast_msg = message.reply_to_message

        # Initialize counters

        total = 0

        successful = 0

        blocked = 0

        deleted = 0

        unsuccessful = 0

        
        # Send a message to the user to let them know the broadcast is starting

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")

        # Loop through the userbase

        for chat_id in query:

            try:

                # Try to copy the message to the user's chat

                await broadcast_msg.copy(chat_id)

                # Increment the successful counter

                successful += 1

            except FloodWait as e:

                # If there is a flood wait, sleep for the specified amount of time

                await asyncio.sleep(e.x)

                # Try to copy the message to the user's chat again

                await broadcast_msg.copy(chat_id)

                # Increment the successful counter

                successful += 1

            except UserIsBlocked:

                # If the user has blocked the bot, delete the user from the userbase

                await del_user(chat_id)

                # Increment the blocked counter

                blocked += 1

            except InputUserDeactivated:

                # If the user has deleted their account, delete the user from the userbase

                await del_user(chat_id)

                # Increment the deleted counter

                deleted += 1

            except:

                # If there is an error, increment the unsuccessful counter

                unsuccessful += 1

                pass

            # Increment the total counter

            total += 1

        
        # Create a status message to send to the user

        status = f"""<b><u>Broadcast Completed</u></b>


<b>Total Users :</b> <code>{total}</code>

<b>Successful :</b> <code>{successful}</code>

<b>Blocked Users :</b> <code>{blocked}</code>

<b>Deleted Accounts :</b> <code>{deleted}</code>

<b>Unsuccessful :</b> <code>{unsuccessful}</code>"""
        
        # Edit the message to show the status

        return await pls_wait.edit(status)

    # If the message is not a reply to another message, send a message to the user

    else:
        msg = await message.reply(f"Use This Command As A Reply To Any Telegram Message With Out Any Spaces.")

        # Wait for 8 seconds

        await asyncio.sleep(8)

        # Delete the message

        await msg.delete()






# Function to handle file deletion

async def delete_files(messages, client, k):

    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py

    for msg in messages:

        try:

            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])

        except Exception as e:

            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    # await client.send_message(messages[0].chat.id, "Your Video / File Is Successfully Deleted ✅")
    
    await k.edit_text("Your Video / File Is Successfully Deleted ✅")



# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
