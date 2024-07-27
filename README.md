# Telegram Scraper

This project scrapes users, channels, and groups on Telegram using the Telethon library. It connects to a Django admin panel for management and is dockerized for easy deployment.

## Features

- Scrape conversations (Groups and Private Chats)
- Scrape users in Groups
- Scrape users in SuperGroups with messages
- Invite users to a target group (specify target group in admin panel)
- Admin panel for managing scrapers and Telegram accounts
- Dockerized for easy setup and deployment

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/itsmohsenjalali/telegram_scraper.git
   cd telegram_scraper
   ```

2. Build and run the Docker containers:

   ```bash
   docker compose build
   docker compose up -d
   ```

3. Create a superuser:

   ```bash
   docker exec -it scraper /bin/bash
   python manage.py createsuperuser
   ```

4. Open your browser and go to the Django admin panel at `http://localhost:8000/admin` and log in with the superuser account.

5. Create your Telegram account in the admin panel and fill in `your_api_id` and `your_api_hash`.

### Running the Scraper

1. Enter the container:

   ```bash
   docker exec -it scraper /bin/bash
   ```

2. Run one of the following commands, authorizing with OTP if prompted:

   - Scrape conversations:

     ```bash
     python manage.py scrape --conversation
     ```

   - Scrape users in Groups:

     ```bash
     python manage.py scrape --user
     ```

   - Scrape users in SuperGroups with messages:

     ```bash
     python manage.py scrape --user_message
     ```

   - Invite users to a target group:

     ```bash
     python manage.py scrape --invite_user_to_group
     ```

   - To run the processes in the background, use `Ctrl+Z` or append `&` to the command.

## Future Development

- Enable running scrapers from the admin panel instead of the terminal.
- Support concurrent scrapers on multiple Telegram accounts.
- Implement precise error handling to prevent Telegram account bans.

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
