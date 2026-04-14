# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for PyAudio and other C-based libraries
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code
COPY . .

# Command to run both the bot and the listener
# Note: Using nohup here might not keep the container alive if bot.py exits.
# Consider using a process manager like supervisord if you need both running reliably.
CMD ["python", "bot.py"]