# Ubuntu latest image use karo
FROM ubuntu:latest  

# Non-interactive mode pe set karo
ENV DEBIAN_FRONTEND=noninteractive  

# Required packages install karo (gcc, python3, pip)
RUN apt update && apt install -y gcc python3 python3-pip  

# Python modules install karo
RUN pip3 install requests psutil python-telegram-bot

# Apna project folder copy karo
COPY . /app  
WORKDIR /app  

# Debugging ke liye check karo ki gcc aur python install hua ya nahi
RUN gcc --version && python3 --version  

# Flooder binary compile karo
RUN gcc m.c -o legacy

# Default command jo chalega jab container run hoga
CMD ["python3", "vps.py"]
