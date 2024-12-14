import os
import time
import pandas as pd

from typing import List, Tuple
from bearer_scraper import get_bearer_token
from database_manager import DatabaseManager
from Logger import Logger
from dotenv import load_dotenv

load_dotenv()
CRON_INTERVAL = int(os.getenv('CRON_INTERVAL', 60))


def read_credentials_from_csv() -> List[Tuple[str, str]]:
    df = pd.read_csv('./credentials.csv')

    df['email'] = df['email'].str.strip()
    df['password'] = df['password'].str.strip()

    # Remove rows with empty email or password
    df = df[df['email'].notna() & (df['email'] != '') &
            df['password'].notna() & (df['password'] != '')]

    credentials = list(zip(df['email'], df['password']))

    Logger.info(f"Successfully read credentials")
    Logger.info(f"Total valid credentials: {len(credentials)}")

    return credentials


def scrape_bearers_from_credentials(credentials: List[Tuple[str, str]]) -> None:
    Logger.info(f"Scraping bearers from {len(credentials)} credentials")
    db = DatabaseManager()
    start_time = time.time()

    # Scrape bearers for each credential
    for email, password in credentials:
        bearer_token = get_bearer_token(email, password)
        db.update_credential(email, bearer_token)

    end_time = time.time()
    Logger.info(f"Scraping completed in {end_time - start_time:.2f} seconds")


def main():
    while True:
        Logger.critical('==================== Starting new run ====================')
        credentials = read_credentials_from_csv()
        scrape_bearers_from_credentials(credentials)
        Logger.info(f'Sleeping for {CRON_INTERVAL} seconds...')
        Logger.info(f'Next run at {time.ctime(time.time() + CRON_INTERVAL)}')
        time.sleep(CRON_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except:
        Logger.critical('Something went wrong', print_exception=True)
    finally:
        Logger.info('Exiting...')
