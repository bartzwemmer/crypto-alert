import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
from yaml import safe_load

from models import Config, MarketChart

LOG = logging.getLogger(__name__)


def generate_chart(market_data: MarketChart, currency: str = "eur") -> Path:
    """
    Generate a chart from the market data and store it as a PNG.
    Returns file path to the PNG file.
    """
    # Extract the dates and prices from the data
    dates = [data[0] for data in market_data["prices"]]
    # convert unix timestamp to datetime
    dates = [datetime.fromtimestamp(date / 1000) for date in dates]
    prices = [data[1] for data in market_data["prices"]]
    # Plot the data
    plt.plot(dates, prices)
    plt.xlabel("Date")
    plt.ylabel("Price (EUR)")
    plt.title("Historical Cardano Price (EUR)")
    Path("./output").mkdir(parents=True, exist_ok=True)
    file_name = f"./output/cardano_price_chart-{currency}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
    plt.savefig(file_name)

    return Path(file_name)


def clean_up_chart(file_name: Path) -> None:
    """
    Delete a Chart PNG (or any file)
    """
    file_name.unlink(missing_ok=True)


def read_config(path: Path = Path("config.yaml")) -> Dict[str, Any]:
    """
    Configure from file in root of the application
    :param path: Path to the .yaml config file
    :return: Settings
    """
    if not path.exists():
        return {}
    with open(path, "r") as f:
        cfg = safe_load(f)

    # Validate the config
    Config(**cfg)

    # TODO extend by reading cfg from env vars and merge results
    return cfg
