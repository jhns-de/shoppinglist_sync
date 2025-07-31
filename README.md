# Shoppinglist Sync

A Python application that synchronizes shopping lists between [Grocy](https://grocy.info/) and CalDAV-compatible calendar applications (like Nextcloud Tasks).

## Features

- **Automatic Sync**: Runs every 15 minutes to keep your shopping lists in sync
- **Unidirectional Updates**: Handles new items and quantity changes
- **Docker Support**: Easy deployment with Docker and Docker Compose

## How it Works

1. Retrieves shopping list items from Grocy
2. Syncs new items to your CalDAV calendar as TODO items
3. Updates quantities when they change in Grocy
4. Maintains sync state in local SQLite database

## Requirements

- Python 3.13+
- Grocy instance with API access
- CalDAV-compatible calendar server (Nextcloud, etc.)

## Installation

### Using Docker (Recommended)

1. Download the `docker-compose.yml` and the `.env.example`
2. Rename `.env.example` in `.env` and configure the environment variables
4. Start the service: `docker-compose up -d`

## Environment Variables

Create a `.env` file or set the following environment variables:

```env
# CalDAV Server Configuration
CALDAV_HOST=https://your-nextcloud-instance.com/remote.php/dav
CALDAV_USER=your-username
CALDAV_PASSWORD=your-password
CALDAV_SHOPPING_LIST_URL=https://your-nextcloud-instance.com/remote.php/dav/calendars/username/shopping-list/

# Grocy Configuration
GROCY_HOST=https://your-grocy-instance.com
GROCY_TOKEN=your-grocy-api-token
```

### Getting Your Configuration

#### CalDAV Setup

- **Nextcloud**: Use your Nextcloud credentials and find the calendar URL in Calendar settings
- **Other CalDAV servers**: Consult your provider's documentation

#### Grocy Setup
1. Log into your Grocy instance
2. Go to "Manage API keys" in user settings
3. Create a new API key
4. Use your Grocy base URL (without `/api`)

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

