import tomllib
import os, logging, datetime
from pydantic import BaseModel

import pandas as pd

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import MessageReactions
import asyncio

from dataclasses import dataclass

LOG_DIR = 'logs'
OUTPUT_DIR = 'output'
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

class TelegramCredentials(BaseModel):
    api_id: int
    api_hash: str
    phone: str
    username: str

@dataclass
class Post:
    text: str
    publication_time: datetime.datetime
    reactions: None | MessageReactions = None

# Load telegram API credentials and other configs from config.toml

def interactive_config():

    print('Configuration file is not found, enter your telegram API credentials!')

    config = {
        'telegram': {
            'api_id': int(input('api_id: ')),
            'api_hash': input('api_hash: '),
            'phone': input('phone: '),
            'username': input('username: ')
        },
        'input': {
            'channels': [input('Link to the telegram channel to scrap: ')]
        },
    }

    print(
        'Configured interactively!',
        'To scrap multiple channels and configure other options, use config.toml file (see tgs_config.toml.example)'
    )

    return config

try:
    with open('tgs_config.toml', 'rb') as f:
        config = tomllib.load(f)
except FileNotFoundError:
    config = interactive_config()


async def init(logger: logging.Logger | None = None) -> TelegramClient:

    # Logging

    if logger is None:

        logger = logging.getLogger('tgscraper')

        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)

        logging.basicConfig(filename=os.path.join(
            LOG_DIR,
            f'tgs_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'),
            level=logging.INFO
        )

    credentials = TelegramCredentials(**config['telegram'])
    os.chdir(LOG_DIR)
    client = TelegramClient(credentials.username, credentials.api_id, credentials.api_hash)

    await client.start()
    if not await client.is_user_authorized():
        await client.send_code_request(credentials.phone)
        try:
            await client.sign_in(credentials.phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    logger.info(f'API credentials and other configs loaded successfully, telegram client started!')

    return client

async def get_posts(client: TelegramClient, channel: str, limit: int = 10):

    posts_df = pd.DataFrame(columns=['text', 'publication_time'])

    async for post in client.iter_messages(channel, limit=limit):

        text = post.message
        if not text:
            continue

        new_post = Post(text, post.date)
        posts_df = pd.concat([posts_df, pd.DataFrame([new_post.__dict__])], ignore_index=True)

    return posts_df

async def main():

    client = await init()

    # Get channels from config, using pattern matching
    if 'input' in config:
        match config['input']:
            case {'channels': channels}: channel_links = channels
            case {'groups': groups}: group_links = groups
            case _: raise ValueError('No channels or groups specified in config!')
    else:
        raise ValueError('No input specified in config!')

    for link in channel_links:
        channel_name = link.split('/')[-1]
        posts_df = await get_posts(client, link, limit=100)

        os.chdir(WORKING_DIR)
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        
        posts_df.to_csv(os.path.join(OUTPUT_DIR, f'{channel_name}.csv'), index=False)
        logger = logging.getLogger('tgscraper')
        logger.info(f'Posts from {channel_name} saved in {OUTPUT_DIR} directory!')

# If the file is running as a script
if __name__ == '__main__':

    # Log to console
    logging.basicConfig(level=logging.INFO)

    # Run the main function
    asyncio.run(main())