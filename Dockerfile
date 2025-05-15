FROM ghcr.io/astral-sh/uv:python3.13-alpine

COPY . /home
WORKDIR /home

RUN uv sync --locked
CMD [ "uv", "run", "main.py" ]
