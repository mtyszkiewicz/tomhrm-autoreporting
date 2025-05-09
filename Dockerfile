FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . .

RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv

ENV PLAYWRIGHT_BROWSERS_PATH=/playwright-browsers

RUN uv pip install --system \
    --no-cache -r requirements.txt

RUN playwright install --with-deps firefox \
    && chmod -Rf 777 $PLAYWRIGHT_BROWSERS_PATH

CMD python3 main.py --scheduled
