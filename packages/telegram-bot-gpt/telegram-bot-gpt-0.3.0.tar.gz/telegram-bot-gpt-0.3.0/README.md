## Telegram-Bot-GPT

A simple interface for OpenAI GPT-3 and GPT-4 using Telegram bots.

**DISCLAIMER**

This open-source module is only intended to provide an interface between bot and AI on top of the following services:
- Bot provided for free by Telegram FZ-LLC
- GPT AI capabilities as paid services from OpenAI LP

The creator of this library is _not in any way responsible_ for any misuse of the module, including but not limited to _any costs that may occur_ due to calls to the GPT AI.

Using this library states that you are agree with this disclaimer.

---

**Installation**
```
pip install telegram-bot-gpt
```

**Usage**
```
import bot_gpt as bot

mybot = bot.Engine("<YOUR_TELEGRAM_TOKEN>")
mybot.set_openai_key("<YOUR_OPENAI_KEY>")  # a filename also accepted

mybot.run()     # only polling method is provided
```

**That's it!!**

---

## Special Features

- Admin now has access to GPT-4
- Using global OTP, changeable and resetable by admin
- A small number of chats are stored encrypted as bot memory
- Used tokens are recorded along with the model, useful for cost calculation
- Modifiable bot parameters

---

## Dev Functions

- Settings

  The variable `bot.DEFAULT_SETTING` contains a dict of the initial values of accessible configurations:

  ```
  {
    "memory_length": 3,        # the number of previous lines involved
    "ai_temperature": 85,      # 0.75 in the API input
    "bot_active": 1,           # 0 is deactivated
    "daily_limit": 50,         # daily usage limit for common users, server time
    "admin_limit": 999,        # daily usage limit for admin, server time
    "password": ""             # will be set automatically at first run
  }
  ```
  
  Accessing variables:
  1. `mybot.set_daily_limit(100)` modify value 
  2. `mybot.reset_daily_limit()` reset to default
  3. `current_daily_limit = mybot.get("daily_limit")` obtain the value
  4. `mybot.reset_settings()` reset all values to default
  <br>


- Bot name
  ```
  mybot.set_botname("My Bot")
  mybot.reset_botname()        # default is "Bot-GPT"
  ```
  <br>

- OpenAI key
  ```
  mybot.set_openai_key("<YOUR_OPENAI_KEY_OR_CORRESPONDING_FILENAME>")
  mybot.del_openai_key()       # AI capabilities will be deactivated
  ```
  <br>

- Memory length, only used when the input is short
  ```
  mybot.set_memory_length(5)   # more value leads to a more expensive cost
  mybot.reset_memory_length()  # default is 3
  memory_length = mybot.get_memory_length()
  ```

---

## Bot Usage

- Admin<br>
  The first user is automatically set as the bot admin which is equipped with a list of commands such as password regulations and bot activations.
  <br><br>

- Password<br>
  New users should enter a randomized code (password) created by the bot which can only be accessed by admin with these commands:

  - `/get_password` displays the current password
  - `/new_passowrd` changes the password without affecting current users
  - `/reset_password` force all users to enter the new password to continue using the bot
  <br><br>

- Deactivation<br>
  The default setting for bot is **active**, whereas only admin has the right to modify it.
  - `/deactivate_bot` bot is off for all users, while **admin still can use it**
  - `/activate_bot` reactivates the bot for all users

  All users can check the bot status using `/is_bot_active`.


---

## How To Get

**Telegram Bot**<br>
Open Telegram app, chat with [@BotFather](https://t.me/BotFather) and send the command /newbot.

**OpenAI key**<br>
Login to [OpenAI](https://platform.openai.com/account/api-keys) and follow the instructions there.
