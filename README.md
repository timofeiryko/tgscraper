# tgscraper

This is a simple package to scrape data from Telegram channels (and other content in the future). It is based on the [Telethon](https://docs.telethon.dev/en/stable/).

It can be used as a CLI tool (saves scraped data to a CSV file) or as a Python package (returns pandas DataFrame).

## Installation

### Install to run as a CLI tool

To use it as a CLI, ptobably the best way to install tgscraper is just to clone this repository and run it from there. We use Poetry to manage dependencies and Python version. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). After that, run the following commands in the root directory of the project:

```bash
poetry install
poetry add tgscraper
```

**To run tgscraper as a script, you need Python 3.11 installed** (otherwise, Poetry will probably fail to create an environment).

Alternatively, you can install dependencies into you own environment without Poetry, using `requirements.txt` file (it can be found in this repository):

```bash
pip install -r requirements.txt
pip install tgscraper
```

### Install to use in your code

#### For poetry

If you use Poetry, just include the dependencies in your `pyproject.toml` file:

```toml
[tool.poetry.dependencies]
python = "^3.11"
pydantic = "^1.10.4"
telethon = "^1.26.1"
pandas = "^1.5.2"
```

Make sure that you don't have any conflicts with the versions of the dependencies.

Then, add tgscraper to your project and install it:

```bash
poetry add tgscraper
poetry install
```

#### For other environment managers

If you use other environment managers, you can install tgscraper using pip:

```bash
pip install -r requirements.txt
pip install tgscraper
```

#### Python version

**To use tgscraper in your code, you need Python 3.11 in the environment that you use.**

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