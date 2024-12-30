from datetime import date

from coingecko import CoinGeckoAPI
from helpers import generate_chart, read_config, clean_up_chart
from models import MarketChart
from slack_client import SlackClient


CONFIG = read_config()

# Initialize CoinGecko API client
coinGecko = CoinGeckoAPI()
# Get historical price data for Bitcoin
coin_data = coinGecko.get_coin_market_chart_by_id(CONFIG["deployment"]["coin"], "eur", "365days")
# Validate response
MarketChart.model_validate(coin_data)

if coin_data["prices"][-1][1] > CONFIG["deployment"]["treshold"]:
    pic_path = generate_chart(CONFIG["deployment"]["coin"], coin_data)
    sc = SlackClient(CONFIG["deployment"]["slack_token"])
    att = [
        {
            "text": f"{CONFIG['deployment']['coin'].capitalize()} prices for the past 24hr on {date.today()}",
            "image_url": sc.get_image_attachment_url(pic_path),
        }
    ]
    sc.post_message(
        CONFIG["deployment"]["slack_channel"],
        f"{CONFIG['deployment']['coin'].capitalize()} is above {CONFIG['deployment']['treshold']} EUR\n {att[0]['image_url']}",
        image_attachment=att,
    )
    clean_up_chart(pic_path)
