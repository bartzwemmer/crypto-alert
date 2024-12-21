from pydantic import BaseModel


class MarketChart(BaseModel):
    # Model for the coinGecko response with a chart
    prices: list[list[int | float]]
    market_caps: list[list[int | float]]
    total_volumes: list[list[int | float]]


class Deployment(BaseModel):
    slack_token: str
    slack_channel: str
    treshold: int | float


class Config(BaseModel):
    # Model for the configuration
    deployment: Deployment
