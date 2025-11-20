FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire panel_exploration package
COPY . /app/panel_exploration

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH=/app

# Expose the port Panel will run on
EXPOSE 5006

# Run the panel app
CMD ["panel", "serve", "panel_exploration/app/playground_app.py", "--address", "0.0.0.0", "--port", "5006", "--allow-websocket-origin", "*"]