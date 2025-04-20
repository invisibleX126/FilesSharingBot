from aiohttp import web

from .route import routes


# Define an asynchronous function called web_server

async def web_server():

    # Create a web application with a maximum client size of 30MB

    web_app = web.Application(client_max_size=30000000)

    # Add the routes to the web application

    web_app.add_routes(routes)

    # Return the web application
    
    return web_app





# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
