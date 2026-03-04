FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /blandskron/
# Copy requirements and install
COPY blandskron/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt gunicorn

# Copy project
COPY . /app/

# Ensure entrypoint is executable
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Collect static files (will use STATIC_ROOT)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["/app/docker-entrypoint.sh"]
