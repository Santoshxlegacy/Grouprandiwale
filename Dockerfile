# Ubuntu base image  
FROM ubuntu:latest  

# Non-interactive mode set karo  
ENV DEBIAN_FRONTEND=noninteractive  

# Python, pip aur dependencies install karo  
RUN apt update && apt install -y python3 python3-pip python3-venv gcc  

# Virtual environment create karo  
RUN python3 -m venv /app/venv  

# Activate virtual env & Install dependencies  
RUN /app/venv/bin/pip install --upgrade pip  
RUN /app/venv/bin/pip install python-telegram-bot requests psutil  

# Project folder copy karo  
COPY . /app  
WORKDIR /app  

# Flooder binary compile karo  
RUN gcc flooder.c -o flooder  

# Default command jo chalega jab container start hoga (Virtual Env ke saath)  
CMD ["/app/venv/bin/python", "script.py"]
