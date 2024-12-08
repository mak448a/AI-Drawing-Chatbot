FROM python:3.13

WORKDIR /app

COPY . .

CMD ["sh", "run.sh"]
