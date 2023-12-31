# Alienware Stock Notifier

This is a portfolio project that utilizes web scraping and Discord API to check the stock availability of Alienware computer monitors on the Dell Refurbished website. When an Alienware item is found in stock, a notification is sent to a designated Discord server.

## Technologies Used
- Python
- Requests library
- BeautifulSoup library
- Discord.py library
- aiohttp library
- asyncio library
- dotenv library

## Setup
Before running the code, make sure you have the necessary dependencies installed and set up a Discord webhook URL. Additionally, ensure that you have the required environment variables set up in a `.env` file.

## Code Overview
The project consists of the following main components:

### 1. Checking Stock and Sending Notification
The `check_stock_and_notify()` function is responsible for checking the stock availability of Alienware items on the Dell Refurbished website. It sends a GET request to the website, scrapes the HTML content using BeautifulSoup, and searches for items with the keyword "Alienware". If an Alienware item is found in stock, it retrieves the product link and image URL, and then calls the `send_discord_notification()` function.

### 2. Sending Discord Notification
The `send_discord_notification(item_name, product_link, product_image)` function is responsible for sending a notification to a designated Discord server using a webhook. It creates a new aiohttp `ClientSession` and a Discord webhook instance using the webhook URL. Then, it composes an embedded message with the item details and sends it to the Discord server.

### 3. Pub/Sub Trigger
The `hello_pubsub(event, context)` function serves as a trigger for the code execution. It is triggered by a message on a Cloud Pub/Sub topic. The function decodes the Pub/Sub message, prints it, and starts the `check_stock_and_notify()` function using asyncio.
