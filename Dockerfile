FROM python:3.12-slim

ENV PLAYWRIGHT_BROWSERS_PATH=/playwright-browsers

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir playwright && \
    playwright install --with-deps firefox && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "main.py", "--schedule"]
