# tgscraper

This is a simple package to scrape data from Telegram channels (and other content in the future). It is based on the [Telethon](https://docs.telethon.dev/en/stable/).

It can be used as a CLI tool (saves scraped data to a CSV file) or as a Python package (returns pandas DataFrame).

## Installation

```bash
pip install tgscraper
```

To use it as a CLI, ptobably the best way to install tgscraper is just to clone this repository and run it from there. We use Poetry to manage dependencies and Python version. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation).

To run tgscraper as a script, you need Python 3.11 installed (otherwise, Poetry will probably fail to create an environment).

## Usage

### Provide API credentials

To run tgscraper you need to provide `tgs_config.toml` file with your API credentials in `tgscraper` directory. You can get them from [my.telegram.org](https://my.telegram.org/). List of channels you want to scrape is also required here. It looks like this (you can find an example in `tgs_config.toml.example` file)

```toml
[telegram]
# api_id = ID HERE (int)
# api_hash = HASH HERE (str)
# phone = PHONE HERE (str)
# username = USERNAME HERE (str)

[input]
channels = ["https://t.me/svtvnews"]
# You can include multiple channels here
```

Alternatively, you can use interactive mode to provide this information (it is enabled automatically if you don't provide `tgs_config.toml` file).

### Run the scraper as a CLI tool

We use Poetry to manage dependencies and build the package. To run the scraper as a CLI tool, you need to run it in Poetry's virtual environment. To do that, run the following command in the root directory of the project:

```bash
poetry run python tgscraper/tgscraper.py
```

The script will create a folder `output` in the root directory of the project if it doesn't exist and save the scraped data there. The name of the file will be the name of the channel.

Alternatively, you can use `poetry shell` to enter the virtual environment and run the scraper just as a regular Python script.

### Use in your code

After pip installing the package, you can use it in your code like this:

```python
from tgscraper import tgscraper
import pandas as pd

# Client a Telegram client
client = tgscraper.init()
# Be aware that you can be prompted to enter your phone number and a code, sent to your Telegram account

# Get the posts from the channel into a pandas DataFrame
posts_df = tgscraper.get_posts(client, link, limit=100)

# Do something with the data
posts_df.to_csv("posts.csv")
```

### Logging

By default, tgscraper saves the logs into `logs` directory, filenames are constructed from date and time. To customize the logging, you can use `BasicConfig` from `logging` module. For example, to log into console, you can use the following code:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

You can also get the logger and customize it:

```python
logger = logging.getLogger("tgscraper")
# Do something with the logger
```

## Contribution

Feel free to open an issue or a pull request if you have any suggestions or found a bug. 