# Use official Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install only production dependencies (no dev tools like jupyter, pytest, flake8)
RUN pip install --no-cache-dir \
    pandas \
    matplotlib \
    seaborn \
    pymongo \
    streamlit \
    Pillow

# Copy the rest of the project code
COPY src/ ./src/
COPY app/ ./app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit dashboard when the container starts
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
