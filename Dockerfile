FROM python:3.9-slim

WORKDIR /app

COPY ./app .

RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN apt-get update && apt-get install -y nmap &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]