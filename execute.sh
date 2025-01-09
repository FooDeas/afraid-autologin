#!/bin/bash
bash -c "PATH=$PATH:/usr/local/bin/; source /app/venv/bin/activate && python /app/autologin.py --headless" |& tee -a /var/log/cron.log 2>&1
