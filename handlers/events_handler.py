import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["BOT_USER_TOKEN"])


@app.message("knock knock")
def ask_who(message, say):
    print(f"********** {message} **************")
    say("_Who's there?_")


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


# Sends a section block with datepicker when someone reacts with a 📅 emoji
@app.event("reaction_added")
def show_datepicker(event, say):
    reaction = event["reaction"]
    if reaction == "calendar":
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Pick a date for me to remind you"},
                "accessory": {
                    "type": "datepicker",
                    "action_id": "datepicker_remind",
                    "initial_date": "2020-05-04",
                    "placeholder": {"type": "plain_text", "text": "Select a date"},
                },
            }
        ]
        say(blocks=blocks, text="Pick a date for me to remind you")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SUPER_APP_TOKEN"])
    handler.start()
