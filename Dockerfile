# Base backend image
FROM python:3.11
WORKDIR /app

# Install Python dependencies first (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src/ ./src/
COPY tokenizer/ /app/tokenizer/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Expose backend port
EXPOSE 8080

CMD ["./start.sh"]