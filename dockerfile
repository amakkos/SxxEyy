FROM selenium/standalone-chrome:latest

# install Python
USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir selenium && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py   /app/main.py
COPY config.py /app/config.py
COPY handler   /app/handler

USER seluser

# ENTRYPOINT  ["python", "main.py"]
ENTRYPOINT ["python", "main.py"]
