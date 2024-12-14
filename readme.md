# Student Beans CC Scraper

## What is this?
This project is a Python-based tool for scraping and managing bearer tokens for the Student Beans website. It automates the process of logging in with provided email and password credentials, retrieving the bearer token, and storing the tokens in a MongoDB database.

## How it Works
1. The `main.py` script reads email and password credentials from a `credentials.csv` file.
2. For each set of credentials, the `bearer_scraper.py` module uses Selenium to log in to the Student Beans website and retrieve the bearer token.
3. The `database_manager.py` module then stores the bearer token in a MongoDB database, updating existing entries or creating new ones as needed.
4. The `main.py` script runs in an infinite loop, checking the credentials and updating the database at a configurable interval (set by the `CRON_INTERVAL` environment variable).

## Setup
1. Clone the repository: `git clone https://github.com/username/student-beans-cc-scraper.git`
2. Install the required Python packages: `pip install -r requirements.txt`
3. Set the necessary environment variables:
   - `MONGODB_URI`: The connection string for your MongoDB database
   - `MONGODB_DB_NAME`: The name of the database to use
   - `CRON_INTERVAL`: The number of seconds between each scraping run (default is 60)
4. Create a `credentials.csv` file in the project directory with the following format:
   ```
   email,password
   user1@example.com,password1
   user2@example.com,password2
   ```

## Running the Scraper
To start the scraper, run the following command:
```
python main.py
```
The scraper will run continuously, updating the database with new bearer tokens as needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.