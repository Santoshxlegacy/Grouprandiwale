# Ubuntu latest image use karo
FROM ubuntu:latest  

# Non-interactive mode pe set karo
ENV DEBIAN_FRONTEND=noninteractive  

# Required packages install karo aur errors check karo
RUN apt update && apt install -y gcc python3 || (cat /var/log/apt/term.log && exit 1)  

# Apna project folder copy karo
COPY . /app  
WORKDIR /app  

# Debugging ke liye check karo ki gcc aur python install hua ya nahi
RUN gcc --version && python3 --version  

# Flooder binary compile karo
RUN gcc flooder.c -o flooder  

# Default command jo chalega jab container run hoga
CMD ["python3", "script.py"]
