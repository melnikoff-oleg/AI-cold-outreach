# Use the official Python 3.12.5 base image
FROM python:3.12.5-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Expose the port for Streamlit (default port is 8501)
EXPOSE 8501

# Run the application
# Run the application with Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
