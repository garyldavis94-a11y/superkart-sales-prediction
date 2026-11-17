FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy backend files, including the trained model
COPY . .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Document the backend API port
EXPOSE 7860

# Start the Flask application using Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:superkart_api"]
