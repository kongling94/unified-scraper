FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
COPY src/ ./src/
RUN pip install --no-cache-dir -e . && \
    playwright install chromium && \
    playwright install-deps

# Copy the rest of the project
COPY . .

# Default command (can be overridden)
CMD ["python", "-m", "unified_scraper"]
