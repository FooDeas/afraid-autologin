FROM python:3-slim

SHELL ["/bin/bash", "-c"]
RUN echo "deb http://deb.debian.org/debian/ stable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y cron xvfb firefox-esr wget vim
RUN wget -c https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && tar -xzf geckodriver-v0.36.0-linux64.tar.gz -C /usr/local/bin/
RUN chown root:root /usr/local/bin/geckodriver

COPY afraid-cron /etc/cron.d/afraid-cron
RUN chmod 0644 /etc/cron.d/afraid-cron
RUN crontab /etc/cron.d/afraid-cron
RUN touch /var/log/cron.log

WORKDIR /app

COPY requirements.txt .
RUN pip3 install virtualenv
RUN virtualenv venv
RUN . /app/venv/bin/activate && pip3 install -r requirements.txt

COPY se-config.toml /root/.cache/selenium/se-config.toml
COPY autologin.py .
COPY settings.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY execute.sh .
RUN chmod +x execute.sh

CMD ./entrypoint.sh
