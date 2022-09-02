# super_freddie
Super Freddie, the Slack bot

## Event Listener
```shell
mkdir secrets
echo "export SUPER_APP_TOKEN='${YOUR_OWN_TOKEN}'" >> secrets/.env
echo "export BOT_USER_TOKEN='${YOUR_OWN_TOKEN}'" >> secrets/.env
. secrets/.env && python handlers/events_handler.py
```
