import pymongo, os

from config import DB_URL, DB_NAME

dbclient = pymongo.MongoClient(DB_URL)

database = dbclient[DB_NAME]

user_data = database['users']



# Define an asynchronous function called present_user that takes a user_id as an argument

async def present_user(user_id : int):

    # Find a user in the user_data collection with the given user_id

    found = user_data.find_one({'_id': user_id})

    # Return True if the user is found, otherwise return False

    return bool(found)

# Define an asynchronous function called add_user that takes an integer parameter user_id

async def add_user(user_id: int):

    # Insert a new document into the user_data collection with the user_id as the _id field

    user_data.insert_one({'_id': user_id})

    # Return nothing

    return

# Define an asynchronous function called full_userbase

async def full_userbase():

    # Find all documents in the user_data collection

    user_docs = user_data.find()

    # Create an empty list to store user IDs

    user_ids = []

    # Loop through each document in the user_docs collection

    for doc in user_docs:

        # Append the user ID from each document to the user_ids list

        user_ids.append(doc['_id'])
        
    # Return the list of user IDs

    return user_ids

# Define an asynchronous function called del_user that takes an integer parameter called user_id

async def del_user(user_id: int):

    # Delete the user data from the database where the user_id matches the parameter

    user_data.delete_one({'_id': user_id})

    # Return nothing
    
    return









# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
