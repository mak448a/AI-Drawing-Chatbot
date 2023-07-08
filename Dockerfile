# Use the official Python image as the base
FROM python:3.12.0b3

# Install necessary packages
RUN apt-get update && apt-get install -y gcc libpq-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the code into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Prompt the user for input and set environment variables
RUN echo "Please enter your Discord bot token: "
RUN read -r BOT_TOKEN
RUN echo "Please enter your Stable Horde API key: "
RUN read -r API_KEY
RUN echo "Please enter your Poe token: "
RUN read -r POE_TOKEN

# Clone the Stable Horde module
RUN git clone https://github.com/mak448a/horde_module --depth=1

# Expose the necessary ports
EXPOSE 80 443

# Start the bot
CMD ["python", "main.py"]
