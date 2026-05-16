"""
Configuration module for the DuckDuckGo Telegram Bot.

This module loads and validates configuration values from environment variables.
It provides typed access to the bot token and admin user IDs.
"""

import os
import sys
from typing import List, Optional

# Environment variable names
BOT_TOKEN_ENV = "BOT_TOKEN"
ADMIN_IDS_ENV = "ADMIN_IDS"


def get_bot_token() -> str:
    """
    Retrieve the Telegram bot token from environment variables.

    Returns:
        str: The bot token.

    Raises:
        SystemExit: If the BOT_TOKEN environment variable is not set or is empty.
    """
    token: Optional[str] = os.environ.get(BOT_TOKEN_ENV)

    if not token:
        print(
            f"Error: {BOT_TOKEN_ENV} environment variable is not set or is empty.",
            file=sys.stderr,
        )
        sys.exit(1)

    return token


def get_admin_ids() -> List[int]:
    """
    Retrieve admin user IDs from environment variables.

    The ADMIN_IDS environment variable should contain a comma-separated list
    of numeric Telegram user IDs (e.g., "123456789,987654321").

    Returns:
        List[int]: A list of admin user IDs. Returns an empty list if the
                   environment variable is not set or is empty.

    Raises:
        SystemExit: If any value in the list is not a valid integer.
    """
    admin_ids_str: Optional[str] = os.environ.get(ADMIN_IDS_ENV)

    if not admin_ids_str:
        return []

    admin_ids: List[int] = []
    parts: List[str] = [part.strip() for part in admin_ids_str.split(",") if part.strip()]

    for part in parts:
        try:
            admin_id: int = int(part)
            admin_ids.append(admin_id)
        except ValueError:
            print(
                f"Error: Invalid admin ID '{part}' in {ADMIN_IDS_ENV}. "
                f"All values must be integers.",
                file=sys.stderr,
            )
            sys.exit(1)

    return admin_ids


# Load configuration values at module import time
BOT_TOKEN: str = get_bot_token()
ADMIN_IDS: List[int] = get_admin_ids()