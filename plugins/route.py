from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)

# Define an asynchronous function called root_route_handler that takes in a request as a parameter

async def root_route_handler(request):

    # Return a JSON response with the string "Madflix_Bots"
    
    return web.json_response("Madflix_Bots")




# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
