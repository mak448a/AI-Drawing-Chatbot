FROM python:bullseye

WORKDIR /app

COPY . .

CMD ["sh", "run.sh"]
