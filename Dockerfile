# Base Docker Image
FROM python:slim

# Copy source code in the container
COPY . /app

# Set Working directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

# Init database
RUN bash setup.sh

# Enable access to the port
EXPOSE 5000

# Launch application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
