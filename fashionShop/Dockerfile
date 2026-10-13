FROM python:3.14-slim

# Prevent Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# System dependencies (install all at once to minimize layers)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libxmlsec1-dev pkg-config build-essential libpq-dev gettext netcat-openbsd gosu && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN django-admin compilemessages

RUN useradd -m -r appuser && chown -R appuser:appuser /app && chmod +x /app/scripts/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

CMD ["gunicorn", "fashionShop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]