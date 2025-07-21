FROM alpine:3.19

# Ensure 'python' points to 'python3'
RUN apk add --no-cache python3 py3-pip build-base libffi-dev rust cargo curl

WORKDIR /app

# Copy requirements first, then install dependencies in venv
COPY requirements.txt .
RUN python3 -m venv /venv \
    && . /venv/bin/activate \
    && pip install --upgrade pip setuptools==78.1.1\
    && pip install -r requirements.txt

# Now copy the rest of the code
COPY . .

# Expose the Gunicorn port
EXPOSE 80

# Use the venv's python/pip/gunicorn
ENV PATH="/venv/bin:$PATH"

# Gunicorn command to start the application
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.interface:create_app()"]
