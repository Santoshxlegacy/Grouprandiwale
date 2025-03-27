# Ubuntu latest image use karo
FROM ubuntu:latest  

# Non-interactive mode set karo
ENV DEBIAN_FRONTEND=noninteractive  

# Python aur GCC install karo
RUN apt update && apt install -y gcc python3 python3-pip  

# Ensure pip is up-to-date
RUN python3 -m pip install --upgrade pip  

# Required Python modules install karo (telegram bot module fixed)
RUN pip3 install --no-cache-dir requests psutil python-telegram-bot==20.0  

# Apna project folder copy karo
COPY . /app  
WORKDIR /app  

# Flooder binary compile karo
RUN gcc m.c -o flooder  

# Default command jo chalega jab container start hoga
CMD ["python3", "vps.py"]
