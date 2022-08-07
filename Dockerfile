FROM python:3.9.5-buster
WORKDIR /app
RUN chmod 777 /app
RUN pip3 install -U pip
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . /app/

EXPOSE 8000

CMD ["python3", "-m", "spr", "runserver", "0.0.0.0:8000"]
