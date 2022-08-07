FROM python:3.9.5-buster
WORKDIR /app
RUN chmod 777 /app
RUN pip3 install -U pip
RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6 -y
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
EXPOSE 5000
RUN chmod +x /app/start.sh
ENTRYPOINT ["./start.sh"]
