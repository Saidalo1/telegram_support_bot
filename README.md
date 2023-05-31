# Support bot for Telegram

<a href="https://hub.docker.com/r/groosha/telegram-report-bot"><img src="https://img.shields.io/badge/Telegram--Bot-blue"></a>

This repository contains source code of a small yet rather powerful bot for Telegram, which handles reports from users
and passes them to admins.
Uses [aiogram](https://github.com/aiogram/aiogram) framework.  
The main goal is to build a bot with no external database needed. Thus, it may lack some features, but hey, it's open
source!

#### Screenshot

![Left - main group. Right - group for admins only. If you don't see this image, please check GitHub repo](https://imgur.com/aXsJ3g3.png)

#### Features

* `/start` to start bot;
* Supports can be sent to a dedicated chat;
* Write message to bot if you are simple user;
* Write reply message to questions if you are owner;
* `/mute` to mute users (muted users can't send message to bot);
* `/unmute` to un mute users;

#### Requirements

* Python 3.9 and above;
* Tested on Linux, should work on Windows, no platform-specific code is used;

#### Installation

1. Go to [@BotFather](https://t.me/telegram), create a new bot, and get token.
2. Clone this repository:

   ```
   git clone https://github.com/Saidalo1/telegram_support_bot.git
   ```
   
3. Open project directory: ```cd telegram_support_bot```
4. Create ***.env*** file to project directory:

   ```
      BOT_TOKEN=YOUR_BOT_TOKEN
      OWNER_ID=OWNER_TELEGRAM_USER_ID
      DATABASE_USER=DATABASE_USER
      DATABASE_PASS=DATABASE_USER_PASSWORD
      DATABASE_HOST=DATABASE_HOST
      DATABASE_NAME=DATABASE_NAME
   ```

##### systemd

1. Create a venv (virtual environment): `python3.9 -m venv venv` (or any other Python 3.9+ version);
2. `source venv/bin/activate && pip install -r requirements.txt`;
3. Rename  `supportbot.service.example` to `supportbot.service` and move it to `/etc/systemd/system`;
4. Open that file and change values for `WorkingDirectory`, `ExecStart` and `EnvironmentFile` providing the correct
   path values;
5. Start your bot and enable its autostart: `sudo systemctl enable supportbot.service --now`;  
6. Check your bots status and logs: `systemctl status supportbot.service`.
