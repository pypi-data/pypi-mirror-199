# database.py

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from typing import Optional

from pybrowsers import helpers
from pybrowsers.database import BROWSERS
from pybrowsers.datatypes import BrowserSettings
from pybrowsers.datatypes import BrowserNotSupportedError
from pybrowsers.datatypes import BrowserDataDB

DB_FILE = Path(__file__).resolve().parent / "browser.db"

logger = helpers.get_logger(__name__)


@contextmanager
def open_db(filename: Path) -> Generator[sqlite3.Cursor, None, None]:
    connection = sqlite3.connect(filename)
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.Error as e:
        logger.error(e)
    finally:
        connection.commit()
        connection.close()


def init_db() -> None:
    with open_db(DB_FILE) as cursor:
        cursor.execute(
            """
            CREATE TABLE if not exists browsers (
                id integer PRIMARY KEY,
                name text NOT NULL UNIQUE,
                command text NOT NULL UNIQUE,
                profile_command text NOT NULL,
                incognito text NOT NULL,
                profile_file text NOT NULL,
                type text
            )
        """
        )


def insert_record(browser: BrowserSettings) -> None:
    logger.info("Inserting browser '%s' in database", browser.name)

    if exists_record(browser.name):
        logger.warning("Ignoring '%s', it exists in database\n", browser.name)
        return None

    with open_db(DB_FILE) as cursor:
        qry = """
            INSERT INTO browsers(name,command,profile_command,incognito,profile_file,type) VALUES(?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            qry,
            (
                browser.name,
                browser.command,
                browser.profile_command,
                browser.incognito,
                browser.profile_file,
                browser.type.name(),
            ),
        )
        if cursor.lastrowid:
            logger.info("Browser '%s' inserted\n", browser.name)
    return None


def exists_record(name: str) -> bool:
    return bool(get_record_by_name(name))


def get_record_by_name(name: str) -> Optional[BrowserDataDB]:
    with open_db(DB_FILE) as cursor:
        cursor.execute("SELECT * from browsers WHERE name = ? LIMIT 1;", (name,))
        result = cursor.fetchall()
        return result[0] if result else None


def remove_record_by_name(name: str) -> None:
    browser = get_record_by_name(name)

    if not browser:
        return None

    with open_db(DB_FILE) as cursor:
        browser_id = browser[0]
        qry = "DELETE from browsers where id = ?"
        cursor.execute(qry, (browser_id,))
        logger.warning("Browser '%s' with id '%s' removed from database\n", name, browser_id)
    return None


def get_browser_config_by_name(name: str) -> BrowserSettings:
    if name not in BROWSERS:
        raise BrowserNotSupportedError(f"Browser '{name}' not supported.")
    return BrowserSettings(**BROWSERS[name])
