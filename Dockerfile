FROM ubuntu:latest
RUN apt update && apt install -y gcc python3
COPY . /app
WORKDIR /app
RUN gcc flooder.c -o flooder
CMD ["python3", "script.py"]
