import os

import logging

from logging.handlers import RotatingFileHandler




# Get the bot token from the environment variables

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Get the API ID from the environment variables

API_ID = int(os.environ.get("API_ID", ""))

# Get the API HASH from the environment variables

API_HASH = os.environ.get("API_HASH", "")



# Get the owner ID from the environment variables

OWNER_ID = int(os.environ.get("OWNER_ID", ""))

# Get the database URL from the environment variables

DB_URL = os.environ.get("DB_URL", "")

# Get the database name from the environment variables

DB_NAME = os.environ.get("DB_NAME", "")


# Get the channel ID from the environment variables

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

# Get the force sub channel ID from the environment variables

FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))


# Get the file auto delete time from the environment variables

FILE_AUTO_DELETE = int(os.getenv("FILE_AUTO_DELETE", "600")) # auto delete in seconds


# Get the port from the environment variables

PORT = os.environ.get("PORT", "8080")

# Get the number of workers for the bot from the environment variables

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))



# Get the admin IDs from the environment variables

try:

    ADMINS=[]

    for x in (os.environ.get("ADMINS", "").split()):

        ADMINS.append(int(x))

except ValueError:
        
        raise Exception("Your Admins list does not contain valid integers.")









# Get the custom caption from the environment variables
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Get the protect content flag from the environment variables
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Get the disable channel button flag from the environment variables
DISABLE_CHANNEL_BUTTON = True if os.environ.get('DISABLE_CHANNEL_BUTTON', "True") == "True" else False

# Get the bot stats text from the environment variables
BOT_STATS_TEXT = "<b>BOT UPTIME :</b>\n{uptime}"







# Get the user reply text from the environment variables
USER_REPLY_TEXT = "❌Don't Send Me Messages Directly I'm Only File Share Bot !"

# Get the start message from the environment variables
START_MSG = os.environ.get("START_MESSAGE", "Hello {mention}\n\nI Can Store Private Files In Specified Channel And Other Users Can Access It From Special Link.")

# Get the force message from the environment variables
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {mention}\n\n<b>You Need To Join In My Channel/Group To Use Me\n\nKindly Please Join Channel</b>")





# Add the owner ID and the default admin ID to the admin list
ADMINS.append(OWNER_ID)
# ADMINS.append(6848088376)

# Set the log file name
LOG_FILE_NAME = "filesharingbot.txt"

# Set up logging
logging.basicConfig(
     
    level=logging.INFO,  # Set the logging level to INFO

    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",  # Set the logging format

    datefmt='%d-%b-%y %H:%M:%S',  # Set the date format

    handlers=[  # Set the handlers for the logger
         
        RotatingFileHandler(  # Create a rotating file handler
             
            LOG_FILE_NAME,  # Set the log file name

            maxBytes=50000000,  # Set the maximum size of the log file

            backupCount=10  # Set the number of backup files to keep

        ),
        logging.StreamHandler()  # Create a stream handler
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


#Define a function called LOGGER that takes a string as an argument and returns a logging.Logger object

def LOGGER(name: str) -> logging.Logger:

    #Get the logger object with the given name
    
    return logging.getLogger(name)
   





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
