FROM intel/intel-optimized-tensorflow:latest
WORKDIR /app
RUN chmod 777 /app
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && apt-get install libgl1 -y
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
CMD ["python3", "-m", "spr"]
