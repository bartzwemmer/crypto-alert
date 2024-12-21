from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def get_image_attachment_url(self, image_path: Path):
        res = self.client.files_upload_v2(file=image_path.as_posix())
        if res.data["ok"]:
            return res.data["file"]["permalink"]
        else:
            raise RuntimeError(res)

    def post_message(
        self, channel: str = None, message: str = None, image_attachment: Path = None
    ):
        if image_attachment:
            message = message + f"\n {image_attachment[0]['image_url']}"

        try:            
            self.client.chat_postMessage(
                channel=channel, text=message, attachments=image_attachment
            )
        except SlackApiError as e:
            raise SlackApiError(e)
