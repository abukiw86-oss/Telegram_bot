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


## how the bot works on telegram 

Delete Message: /delete (reply to message)

Unmute User: /unmute (reply to muted user's message)

List Muted Users: /muted - shows all muted users

Clear Messages:

/clear 50 - clear last 50 messages

/clear now - clear immediately

Self-Destruction:

/destroy 30d - destroy in 30 days

/destroy 12h - destroy in 12 hours

/destroy 45m - destroy in 45 minutes

/cancel_destroy - cancel scheduled destruction

Remove User by Username: /remove_user @username