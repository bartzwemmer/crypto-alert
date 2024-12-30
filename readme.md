# Crypto alert
This python library allows you to monitor the price of a crypto currency and send you an email when the price reaches a certain threshold. It uses the CoinGecko API to get the price of the crypto currency.

## Configuration
You can specify configuration through a yaml file or environment variables.
### YAML configuration
To use this library, you need to create a config.yaml file in the root directory of the project. The config.yaml file should contain the following information:
```yaml
crypto:
  coin: "coin name"
deployment:
  slack_token: "slack access token"
  slack_channel: "slack channel name"
  treshold: 0.5 # treshold value in euro, will send notiification when price is above this value
```
### Environment variables
To offer a safe way of providing confidential information, the slack token can be provided as an environment variable:
```bash
export SLACK_TOKEN=slack_token
```