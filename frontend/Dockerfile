
# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy frontend application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit application port
EXPOSE 8501

# Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
