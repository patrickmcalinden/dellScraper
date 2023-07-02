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
    try:
        print("Sending request to", URL)
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for non-2xx response codes
        print("Received response:", response.status_code)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all HTML elements with the specified class
        items = soup.find_all("span", class_="model")
        print("Found", len(items), "items on the page")

        # Check if any item contains the keyword "Alienware"
        found_item = False
        for item in items:
            if "Alienware" in item.text:
                found_item = True
                print("Found Item")
                product_link = item.find_previous("a")["href"]
                product_image = 'https://www.dellrefurbished.com'
                product_image += item.find_previous("div", class_="thumb-grid").find("img")['data-src']
                await send_discord_notification(item.text, product_link, product_image)

        if not found_item:
            print("No item found matching 'Alienware'")

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)

# Function to send a Discord notification
async def send_discord_notification(item_name, product_link, product_image):
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
    try:
        print("Sending Discord notification for item:", item_name)
        # Create a new aiohttp ClientSession
        async with aiohttp.ClientSession() as session:
            # Create a new Discord webhook instance
            webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)

            # Compose the embedded message
            embed = discord.Embed(title="Item in Stock", description=item_name, color=discord.Color.green())
            embed.add_field(name="Product Link", value=product_link, inline=False)
            embed.set_image(url=product_image)

            # Send the embedded message
            await webhook.send(embed=embed)

        print("Discord notification sent for item:", item_name)

    except aiohttp.ClientError as e:
        print("Error occurred while sending Discord notification:", e)

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print("Pub Sub Message:", pubsub_message)
    print('Starting Check')
    asyncio.run(check_stock_and_notify())
    print('Finished Check')