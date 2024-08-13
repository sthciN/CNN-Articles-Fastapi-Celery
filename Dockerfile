FROM python:3.12

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python - \
    && echo "export PATH=\"$HOME/.poetry/bin:$PATH\"" >> ~/.bashrc

SHELL ["/bin/bash", "-c", "source ~/.bashrc"]

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

CMD ["bash", "startup.sh"]