FROM python:3.13

# Instalace požadavků
COPY ./requirements.txt /
RUN pip install --upgrade pip uwsgi
RUN pip install -r /requirements.txt

# Vytvoření uživatele
ARG UID=1000
ARG GID=1000

RUN groupadd -g "${GID}" admin \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" admin

# Spouštěcí skript
COPY ./start.sh /
RUN chmod +x /start.sh

# Zkopíruj celý projekt (včetně manage.py) do /app
COPY . /app

# Nastavení pracovního adresáře a uživatele
WORKDIR /app
USER admin

# Kontejnerová metadata
EXPOSE 80
VOLUME [ "/data", "/app" ]

# Výchozí spuštění
ENTRYPOINT [ "/start.sh" ]
CMD [ "uwsgi" ]
