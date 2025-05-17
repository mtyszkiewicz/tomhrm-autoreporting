# tomhrm-autoreporting

Automate daily work time reporting in the tomHRM system.  
Install once and forget about manual input.

## Limitations
 - No support for project selection
 - Report schedule is hardcoded
 - Only supports username/password authentication

Feel free to fork the repo or submit a pull request if you’d like to add these or other features!

## Quick Start (Docker)
1. Clone the repository:
```sh
git clone https://github.com/mtyszkiewicz/tomhrm-autoreporting.git
cd tomhrm-autoreporting
```
2. Create a `.env` file in the root directory with your credentials:
```sh
TOMHRM_USERNAME=your@email.com
TOMHRM_PASSWORD=yourpassword
TOMHRM_WORKSPACE=your-workspace-name
```
3. Run the app:
```sh
docker compose up
```

## Advanced Usage & Development

Use this setup if you want to run the script manually, modify the code, or contribute.

1. Install dependencies

Depending on your environment:
```bash
# Using uv
uv sync
playwright install firefox  # Or your browser engine of choice
```
```bash
# Using Poetry
poetry install
playwright install firefox
```
```bash
# Using pip
pip install schedule playwright
playwright install firefox
```

2. Set environment variables

You can export them manually, or use a tool like [direnv](https://direnv.net/) to automate this.
```bash
#!/usr/bin/env bash
export TOMHRM_USERNAME=""
export TOMHRM_PASSWORD=""
export TOMHRM_WORKSPACE=""
```

3. Run the script

**Run once immediately:**
```bash
python3 main.py
```

**Run with browser visible (headed mode):**
```bash
python3 main.py --headed
```

**Run on a schedule (uses hardcoded timing):**
```bash
python3 main.py --schedule
```

**Save screenshots on error:**
```bash
python3 main.py --screenshot-dir ./screenshots
```