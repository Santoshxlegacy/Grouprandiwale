# Ubuntu base image
FROM ubuntu:latest  

# Non-interactive mode set karo
ENV DEBIAN_FRONTEND=noninteractive  

# Python, pip aur dependencies install karo
RUN apt update && apt install -y python3 python3-pip gcc  

# Ensure pip is updated
RUN python3 -m pip install --upgrade pip  

# Force install telegram module (Break System Packages flag use karke)
RUN pip3 install --break-system-packages python-telegram-bot requests psutil  

# Project folder copy karo
COPY . /app  
WORKDIR /app  

# Flooder binary compile karo
RUN gcc flooder.c -o flooder  

# Default command jo chalega jab container start hoga
CMD ["python3", "script.py"]
