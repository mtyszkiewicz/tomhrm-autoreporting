# tomhrm-autoreporting

Browser automation to report 8 hours to your default project every day at 17:00.

## Limitations
 - No support for project selection (uses default)
 - Hardcoded schedule (17:00)
 - Only supports username/password authentication

*Pull requests to address these limitations are welcome.*

## Quick Start (Docker)
1. **Clone the repository:**
```bash
git clone https://github.com/mtyszkiewicz/tomhrm-autoreporting.git
cd tomhrm-autoreporting
```
2. **Configure credentials:**
Create a `.env` file in the root directory:
```.env
TOMHRM_USERNAME=your@email.com
TOMHRM_PASSWORD=yourpassword
TOMHRM_WORKSPACE=your-workspace-name
```
3. **Run:**
```bash
docker compose up -d
```

## Notifications
The script uses [Apprise](https://pypi.org/project/apprise/) to notify you on failures (e.g., unexpected 2FA or layout changes).

To enable **Telegram** notifications, add these to your `.env` file:
```.env
TELEGRAM_BOT_TOKEN=yourbottoken
TELEGRAM_CHAT_ID=111222333444
```

## Local Development

Use this setup to run the script manually or contribute code.

1. **Install Dependencies**

Using uv:
```bash
uv sync
playwright install firefox
```

Using poetry:
```bash
poetry install
playwright install firefox
```

2. **Set Environment Variables**

Export these manually or use [direnv](https://direnv.net/):
```bash
export TOMHRM_USERNAME="your@email.com"
export TOMHRM_PASSWORD="yourpassword"
export TOMHRM_WORKSPACE="your-workspace-name"  
```

3. **Usage**

```bash
# Run once immediately
python3 main.py

# Run with browser visible (debug mode)
python3 main.py --headed

# Run on schedule (loop forever)
python3 main.py --schedule

# Save screenshots on error
python3 main.py --screenshot-dir ./screenshots
```