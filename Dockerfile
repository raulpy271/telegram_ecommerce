# Use Python 3.8 as base image
FROM python:3.10 AS dev

# Set working directory to /app
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

FROM dev AS prod
# Copy files to /app directory
COPY . /app

# Run script.py when container launches
CMD ["python", "bot.py"]