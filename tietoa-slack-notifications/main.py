import httpx
import models
import slack_sdk
from config import settings
from loguru import logger


def fetch_userdata() -> list[models.UserOutputModel]:
    headers = {"Authorization": f"Bearer {settings.grist_api_key}"}

    with httpx.Client() as client:
        response = client.get(
            f"{settings.grist_api_url}/{settings.grist_api_userdoc}/tables/{settings.grist_api_usertable}/records",
            headers=headers,
        )

        lst = [x["fields"] for x in response.json()["records"]]

        return [models.UserOutputModel(**x) for x in lst]


def filter_users(users: list[models.UserOutputModel]):
    return [user for user in users if user.notifications]


def build_block(message: str):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message,
        },
    }


def main():
    users = fetch_userdata()
    filtered_users = filter_users(users)

    client = slack_sdk.WebClient(token=settings.slack_bot_token)

    for user in filtered_users:
        msg = f"Terve <@{user.user}>! Muista vastata kiirekyselyyn:\n> <https://tie.up.railway.app/kiire/{user.username}>"

        client.chat_postMessage(channel=user.user, blocks=[build_block(msg)], text=msg)


if __name__ == "__main__":
    main()
