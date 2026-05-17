FROM python:3.11-slim

# Install curl + git (needed for cloning + installs)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Syft & Grype(needed for sbom generation and vulnerability scanning)
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]