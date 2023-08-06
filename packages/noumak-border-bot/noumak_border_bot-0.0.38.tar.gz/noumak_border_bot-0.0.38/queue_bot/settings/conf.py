import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent.absolute()
dorenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dorenv_path):
    load_dotenv(dorenv_path)


LOCALES_DIRS = BASE_DIR / "locales"
I18N_DOMAIN = "mybot"


headers = {
    "authority": "mon.declarant.by",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Origin": "https://mon.declarant.by",
}

admin_id = os.getenv("ADMIN_ID")
token = os.getenv("TOKEN")

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "5432",
                "user": db_user,
                "password": db_password,
                "database": "tele_bot",
            },
        },
    },
    "apps": {
        "models": {
            "models": ["queue_bot.db.models"],
            "default_connection": "default",
        }
    },
}
