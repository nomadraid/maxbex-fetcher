#!/bin/sh
# Entrypoint for data pipeline service, which runs the initialisation script and creates crontab for data monitoring and updating

python /app/init.py &
echo "0 * * * * /usr/local/bin/python /app/update.py" | crontab -
crond -l 2 -f &
wait