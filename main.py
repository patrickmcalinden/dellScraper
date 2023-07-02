import base64
import requests
from bs4 import BeautifulSoup
import discord
import aiohttp
import asyncio
import os 
from dotenv import find_dotenv, load_dotenv

# Finding env variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Function to check if Alienware item is in stock and send Discord notification
async def check_stock_and_notify():
    URL = "https://www.dellrefurbished.com/computer-accessories/computer-monitors"
    # Send a GET request to the website URL
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all HTML elements with the specified class
    items = soup.find_all("span", class_="model")

    # Check if any item contains the keyword "Alienware"
    for item in items:
        if "Alienware" in item.text:
            product_link = item.find_previous("a")["href"]
            product_image = 'https://www.dellrefurbished.com'
            product_image += item.find_previous("div", class_="thumb-grid").find("img")['data-src']
            await send_discord_notification(item.text,product_link,product_image)

# Function to send a Discord notification
async def send_discord_notification(item_name,product_link,product_image):
    # Get env variable
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    # Create a new aiohttp ClientSession
    async with aiohttp.ClientSession() as session:
        # Create a new Discord webhook instance
        webhook = discord.Webhook.from_url(WEBHOOK_URL,session=session)
        # Compose the embedded message
        embed = discord.Embed(title="Item in Stock", description=item_name, color=discord.Color.green())
        embed.add_field(name="Product Link", value=product_link, inline=False)
        embed.set_image(url=product_image)
        # Send the embedded message
        await webhook.send(embed=embed)

# Google Function that takes in event trigger and calls main function
def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print("Pub Sub Message : " + pubsub_message)
    # Calling MY function
    print('Starting Check')
    asyncio.run(check_stock_and_notify())
    print('Finished Check')
