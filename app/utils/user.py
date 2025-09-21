from .colors import YELLOW, RESET
from requests import get

def check_version(version) -> str:
    """Check for the new version of the script."""
    try:  # Try ot get the version of the bot.
        last_release = get('https://pastebin.com/raw/kRqGGUkc').text
        return f'\n{YELLOW}Version {last_release} is available!{RESET}' \
            if version != last_release else ''
            
    except Exception:  # SSL error.
        return f'\n{YELLOW}Unable to get the latest version.{RESET}'