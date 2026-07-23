## Project Structure 

```graph 

-telegram_greeting_bot/
├── main.py
├── config.py
├── utils/
│   ├── __init__.py
│   └── decorators.py
├── handlers/
│   ├── __init__.py
│   ├── admin_handler.py
│   ├── user_handler.py
│   └── cleanup_handler.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── cleanup_service.py
│   └── admin_service.py
└── models/
    ├── __init__.py
    └── user.py

```


# Telegram Bot

A feature-rich Telegram group management bot with admin controls and automated moderation.

## Features

- 👋 Welcome new members
- 💔 Farewell messages for leaving members
- 👑 Admin-only commands:
  - Ban users
  - Mute/Unmute users
  - List muted users
  - Delete messages
  - Clear messages (bulk delete)
  - Remove users by username
  - Schedule group self-destruction
  - Cancel scheduled destruction
 
## Local Development

1. Clone the repository
2. Create a `.env` file with your `BOT_TOKEN`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

## Bot Commands
/ban - Ban a user (reply to their message)
/mute - Mute a user (reply to their message)
/unmute - Unmute a user (reply to their message)
/muted - List all muted users
/delete or /purge - Delete a message (reply to it)
/clear <count|now> - Clear messages
/remove_user @username - Remove user by username
/destroy <time> - Self-destruct group (30d/12h/45m)
/cancel_destroy - Cancel scheduled destruction

text

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| BOT_TOKEN | Telegram Bot Token | Yes |
| DEFAULT_EXPIRY_YEARS | Default group destruction time | No (default: 10) |
| LOG_LEVEL | Logging level (INFO, DEBUG, etc.) | No (default: INFO) |

## Note

- Only group admins can execute moderation commands
- The bot needs appropriate admin permissions in the group