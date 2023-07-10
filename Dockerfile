FROM python:bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the code into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Clone the Stable Horde module
RUN git clone https://github.com/mak448a/horde_module --depth=1

# Expose the necessary ports
EXPOSE 80 443

# Start the bot
CMD ["sh", "run.sh"]
