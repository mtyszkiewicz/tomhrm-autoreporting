## tomhrm-autoreporting

- does not support project selection
- the report schedule is hardcoded
- auth method is only username/password

feel encouraged to make a PR / fork the repo if you need these or other features

## Setup

1.  **Clone the repo.**
```bash
git clone git@github.com:mtyszkiewicz/tomhrm-autoreporting.git
```
```bash
git clone https://github.com/mtyszkiewicz/tomhrm-autoreporting.git
```
2.  **Install dependencies:**
```bash
    uv sync
    playwright install firefox  # Or your browser of choice if modified
```
```bash
    poetry install
    playwright install firefox
```
```bash
    pip install schedule playwright
    playwright install firefox
```
3.  **Set Environment Variables:** (I use [direnv](https://direnv.net/))
```bash
#!/usr/bin/env bash
export TOMHRM_USERNAME=""
export TOMHRM_PASSWORD=""
export TOMHRM_WORKSPACE=""
```

## Usage

**Run once immediately:**
```bash
python3 main.py
```

**Run once in headed mode (to see the browser):**
```bash
python3 main.py --headed
```

**Run on a schedule (uses hardcoded values):**
```bash
python3 main.py --schedule
```

**Specify screenshot directory for capturing errors**
```bash
python3 main.py --screenshot-dir ./screenshots
```