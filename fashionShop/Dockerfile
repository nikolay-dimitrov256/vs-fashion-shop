FROM python:3.13.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd -ms /bin/bash appuser

WORKDIR /app

# System dependencies (install all at once to minimize layers)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libxmlsec1-dev pkg-config build-essential libpq-dev gcc gettext netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]