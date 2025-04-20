# Import the web module from aiohttp

from aiohttp import web

# Import the web_server module from plugins

from plugins import web_server

# Import the listen module from pyromod

import pyromod.listen

# Import the Client module from pyrogram

from pyrogram import Client

# Import the ParseMode module from pyrogram.enums

from pyrogram.enums import ParseMode

# Import the sys module

import sys

# Import the datetime module

from datetime import datetime

from config import API_HASH, API_ID, LOGGER, BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

import pyrogram.utils

# Set the minimum channel ID to -1009999999999
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999



class Bot(Client):
    
    def __init__(self):

        # Initialize the Bot class by calling the parent class (Client) and passing in the necessary parameters

        super().__init__(

            name="Bot",

            api_hash=API_HASH,

            api_id=API_ID,

            plugins={"root": "plugins"},

            workers=TG_BOT_WORKERS,

            bot_token=BOT_TOKEN

        )

        # Set the LOGGER variable to the LOGGER object

        self.LOGGER = LOGGER

    async def start(self):

        # Start the bot by calling the parent class (Client) and getting the bot's username

        await super().start()

        usr_bot_me = await self.get_me()

        self.uptime = datetime.now()

        # Check if FORCE_SUB_CHANNEL is set and if the bot can export an invite link from it

        if FORCE_SUB_CHANNEL:

            try:

                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link

                if not link:

                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)

                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link

                self.invitelink = link

            except Exception as a:

                self.LOGGER(__name__).warning(a)

                self.LOGGER(__name__).warning("Bot Can't Export Invite link From Force Sub Channel!")

                self.LOGGER(__name__).warning(f"Please Double Check The FORCE_SUB_CHANNEL Value And Make Sure Bot Is Admin In Channel With Invite Users Via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")

                self.LOGGER(__name__).info("\nBot Stopped. https://t.me/MadflixBots_Support For Support")

                sys.exit()

        # Check if the bot is an admin in the DB channel and if the CHANNEL_ID is set correctly
        try:
            db_channel = await self.get_chat(CHANNEL_ID)

            self.db_channel = db_channel

            test = await self.send_message(chat_id = db_channel.id, text = "Hey 🖐")

            await test.delete()

        except Exception as e:

            self.LOGGER(__name__).warning(e)
            
            self.LOGGER(__name__).warning(f"Make Sure Bot Is Admin In DB Channel, And Double Check The CHANNEL_ID Value, Current Value: {CHANNEL_ID}")

            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/MadflixBots_Support For Support")

            sys.exit()

        # Set the parse mode to HTML and log the bot's username

        self.set_parse_mode(ParseMode.HTML)

        self.LOGGER(__name__).info(f"Bot Running...!\n\nCreated By \nhttps://t.me/Madflix_Bots")

        self.LOGGER(__name__).info(f"""ミ💖 MADFLIX BOTZ 💖彡""")

        self.username = usr_bot_me.username

        #web-response

        app = web.AppRunner(await web_server())

        await app.setup()

        bind_address = "0.0.0.0"

        await web.TCPSite(app, bind_address, PORT).start()


    async def stop(self, *args):

        # Stop the bot by calling the parent class (Client) and logging the stop message

        await super().stop()
        
        self.LOGGER(__name__).info("Bot Stopped...")
            





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
