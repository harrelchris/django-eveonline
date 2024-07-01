import urllib.request

from django.conf import settings
from django.db import connection

COMMANDS = {
    "enable": {
        "sqlite3": "PRAGMA foreign_keys = ON;",
        "postgresql": "SET session_replication_role = 'origin';",
        "mysql": "SET FOREIGN_KEY_CHECKS=1;",
    },
    "disable": {
        "sqlite3": "PRAGMA foreign_keys = OFF;",
        "postgresql": "SET session_replication_role = 'replica';",
        "mysql": "SET FOREIGN_KEY_CHECKS=0;",
    },
}


def get_remote_hash() -> str:
    request = urllib.request.Request(
        url="https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2.md5",
    )
    response = urllib.request.urlopen(request)
    content = response.read()
    return content.decode("utf-8").strip()


def disable_foreign_key_verification():
    engine = settings.DATABASES["default"]["ENGINE"].split(".")[-1]
    with connection.cursor() as cursor:
        command = COMMANDS["disable"][engine]
        cursor.execute(command)


def enable_foreign_key_verification():
    engine = settings.DATABASES["default"]["ENGINE"].split(".")[-1]
    with connection.cursor() as cursor:
        command = COMMANDS["enable"][engine]
        cursor.execute(command)
