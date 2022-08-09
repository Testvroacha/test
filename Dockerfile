FROM python:3.9.5-buster
WORKDIR /app
RUN chmod 777 /app
RUN apt-get update
RUN apt-get install libgl1 
RUN apt-get install libcudart.so.11.0
RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
CMD ["python3", "-m", "spr"]
