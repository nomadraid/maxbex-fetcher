# Data pipeline service

FROM python:3.9-alpine
USER root 
WORKDIR /app 
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY init.py ./init.py
COPY update.py ./update.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
