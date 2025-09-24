# Use an official Python runtime as a parent image
# 'slim' is a lightweight version, which is good for production
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the file that lists our dependencies
COPY requirements.txt .

# Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application code into the container
COPY . .

# Tell Docker that the container listens on port 8000
EXPOSE 8000

# The command to run when the container starts.
# We use 0.0.0.0 to make it accessible from outside the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]