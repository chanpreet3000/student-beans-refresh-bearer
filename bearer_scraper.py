import time

from typing import Optional
from seleniumbase import SB
from seleniumbase.config import settings

from Logger import Logger


def get_bearer_token(email: str, password: str, max_retries: int = 3) -> Optional[str]:
    details = {
        'email': email,
        'password': password
    }
    for attempt in range(max_retries):
        try:
            Logger.info(f'Fetching bearer token. Attempt {attempt + 1}/{max_retries}', details)
            with SB(uc=True, incognito=True, headless=True) as sb:
                Logger.debug("Navigating to login page")
                sb.uc_open('https://accounts.studentbeans.com/in/authorisation/log-in')
                Logger.info("Navigated to login page")

                Logger.debug('Accepting cookies')
                sb.uc_click('button#onetrust-accept-btn-handler',
                            by="css selector",
                            timeout=settings.SMALL_TIMEOUT,
                            reconnect_time=None)
                Logger.info('Accepted cookies')

                Logger.debug('Typing email and password')
                sb.type('#email', email)
                sb.type('#password', password)
                Logger.info('Typed email and password')

                Logger.debug('Clicking login button')
                sb.uc_click(
                    "#authorisation_root > div > div > div.css-ouos42 > div.css-1d0nbku > form > div:nth-child(4) > button",
                    by="css selector",
                    timeout=settings.SMALL_TIMEOUT,
                    reconnect_time=None)
                Logger.info('Clicked login button')

                # waiting for login
                time.sleep(5)

                # navigating to studentbeans
                Logger.debug('Navigating to studentbeans')
                sb.uc_open("https://www.studentbeans.com/in")
                Logger.info('Navigated to studentbeans')

                Logger.debug('Accepting main page cookies')
                sb.uc_click('button#onetrust-accept-btn-handler',
                            by="css selector",
                            timeout=settings.SMALL_TIMEOUT,
                            reconnect_time=None)
                Logger.info('Accepted main page cookies')

                Logger.debug('Clicking login button')
                sb.uc_click('[data-testid="nav-login"]',
                            by="css selector",
                            timeout=settings.SMALL_TIMEOUT,
                            reconnect_time=None)
                Logger.info('Clicked login button')

                Logger.debug('Refreshing page')
                sb.refresh()
                Logger.info('Refreshed page')

                time.sleep(2)

                cookies = sb.get_cookies()
                Logger.debug('Fetched cookies')
                for cookie in cookies:
                    if cookie['name'] == 'viewer_token':
                        bearer = cookie['value']
                        Logger.info('Found token:', {
                            'details': details,
                            'bearer': bearer
                        })
                        return bearer

                Logger.warning(f'Bearer token not found', details)

        except:
            Logger.error(f"Error fetching bearer token", details, print_exception=True)

    Logger.error(f"Failed to fetch bearer token", details)
    return None
