# Import the base64 module to encode and decode data
import base64

# Import the re module to use regular expressions
import re

# Import the asyncio module to handle asynchronous operations
import asyncio

# Import the filters module from pyrogram to filter messages
from pyrogram import filters

# Import the ChatMemberStatus enum from pyrogram to check the status of a chat member
from pyrogram.enums import ChatMemberStatus

# Import the FORCE_SUB_CHANNEL and ADMINS variables from the config module
from config import FORCE_SUB_CHANNEL, ADMINS

# Import the UserNotParticipant exception from pyrogram to handle the case where a user is not a participant of a channel
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

# Import the FloodWait exception from pyrogram to handle the case where the bot is being rate limited
from pyrogram.errors import FloodWait




# Define an asynchronous function called is_subscribed that takes in three parameters: filter, client, and update
async def is_subscribed(filter, client, update):

    # If FORCE_SUB_CHANNEL is not set, return True

    if not FORCE_SUB_CHANNEL:

        return True
    
    # Get the user_id from the update

    user_id = update.from_user.id

    # If the user_id is in the ADMINS list, return True

    if user_id in ADMINS:

        return True
    
    # Try to get the chat member from the FORCE_SUB_CHANNEL

    try:

        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL, user_id = user_id)

    # If the user is not a participant, return False

    except UserNotParticipant:

        return False

    # If the member's status is not in the list of OWNER, ADMINISTRATOR, or MEMBER, return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:

        return False
    
    # Otherwise, return True

    else:

        return True 


# Define an asynchronous function called encode that takes a string as an argument

async def encode(string):

    # Encode the string into bytes using ASCII encoding

    string_bytes = string.encode("ascii")

    # Encode the bytes into base64 using URL-safe encoding

    base64_bytes = base64.urlsafe_b64encode(string_bytes)

    # Decode the base64 bytes into a string using ASCII encoding

    base64_string = (base64_bytes.decode("ascii")).strip("=")

    # Return the base64 string

    return base64_string


async def decode(base64_string):    # This function is used to decode the base64 string

    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.

    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")

    string_bytes = base64.urlsafe_b64decode(base64_bytes) 

    string = string_bytes.decode("ascii")

    return string


# Define an asynchronous function called get_messages that takes in a client and a list of message_ids

async def get_messages(client, message_ids):

    # Initialize an empty list to store the messages

    messages = []

    # Initialize a variable to keep track of the total number of messages

    total_messages = 0
    # Loop until the total number of messages is equal to the length of the message_ids list

    while total_messages != len(message_ids):

        # Slice the message_ids list to get a list of 200 message_ids

        temb_ids = message_ids[total_messages:total_messages+200]

        # Try to get the messages from the client's database channel using the sliced message_ids list

        try:

            msgs = await client.get_messages(

                chat_id=client.db_channel.id,

                message_ids=temb_ids
            )

        # If a FloodWait exception is raised, wait for the specified amount of time and then try again

        except FloodWait as e:

            await asyncio.sleep(e.x)

            msgs = await client.get_messages(

                chat_id=client.db_channel.id,

                message_ids=temb_ids

            )

        # If any other exception is raised, pass
        except:

            pass

        # Increment the total number of messages by the length of the sliced message_ids list

        total_messages += len(temb_ids)

        # Extend the messages list with the messages retrieved from the client's database channel

        messages.extend(msgs)

    # Return the messages list

    return messages



# Define an asynchronous function to get the message ID from a given message

async def get_message_id(client, message):

    # Check if the message is forwarded from a chat

    if message.forward_from_chat:

        # Check if the forwarded chat is the same as the database channel

        if message.forward_from_chat.id == client.db_channel.id:

            # Return the forwarded message ID

            return message.forward_from_message_id
        
        else:

            # Return 0 if the forwarded chat is not the same as the database channel

            return 0
        
    # Check if the message has a forward sender name

    elif message.forward_sender_name:

        # Return 0 if the message has a forward sender name

        return 0
    
    # Check if the message has text

    elif message.text:

        # Define a pattern to match the message text

        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"

        # Match the pattern with the message text

        matches = re.match(pattern,message.text)

        # Check if the pattern matches

        if not matches:

            # Return 0 if the pattern does not match

            return 0
        
        # Get the channel ID from the matched pattern

        channel_id = matches.group(1)

        # Get the message ID from the matched pattern

        msg_id = int(matches.group(2))

        # Check if the channel ID is a digit

        if channel_id.isdigit():

            # Check if the channel ID is the same as the database channel ID

            if f"-100{channel_id}" == str(client.db_channel.id):

                # Return the message ID if the channel ID is the same as the database channel ID

                return msg_id
        else:

            # Check if the channel ID is the same as the database channel username

            if channel_id == client.db_channel.username:

                # Return the message ID if the channel ID is the same as the database channel username

                return msg_id
            
    else:

        # Return 0 if the message does not have text

        return 0


def get_readable_time(seconds: int) -> str:

    # Initialize count and up_time variables

    count = 0

    up_time = ""

    # Create an empty list to store the time values

    time_list = []

    # Create a list of time suffixes

    time_suffix_list = ["s", "m", "h", "days"]

    # Loop through the time suffix list

    while count < 4:

        # Increment count

        count += 1

        # If count is less than 3, divide seconds by 60, otherwise divide by 24

        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)

        # If seconds is 0 and remainder is 0, break the loop

        if seconds == 0 and remainder == 0:

            break

        # Append the result to the time_list

        time_list.append(int(result))

        # Update seconds with the remainder

        seconds = int(remainder)

    # Get the length of the time_list

    hmm = len(time_list)

    # Loop through the time_list

    for x in range(hmm):

        # Append the time suffix to the time_list

        time_list[x] = str(time_list[x]) + time_suffix_list[x]

    # If the length of the time_list is 4, append the first element to up_time

    if len(time_list) == 4:

        up_time += f"{time_list.pop()}, "

    # Reverse the time_list

    time_list.reverse()

    # Join the time_list with colons and append to up_time

    up_time += ":".join(time_list)

    # Return up_time

    return up_time


# Create a filter to check if a user is subscribed

subscribed = filters.create(is_subscribed)
       





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
