FROM ubuntu:latest
RUN apt update && apt install -y gcc python3
RUN pip install python-telegram-bot
COPY . /app
WORKDIR /app
RUN gcc m.c.c -o legacy
CMD ["python3", "vps.py"]
