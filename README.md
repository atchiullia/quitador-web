# Quitador Web

**Quitador Web** is a professional, modular web application for simulating loan payoff strategies using the Snowball method.  
It is built with Flask, follows Clean Architecture and DDD principles, and supports Dockerized deployment with Redis-backed sessions.

---

## 🚀 Features

- **Dynamic Web Form:** Add multiple loans dynamically via the web interface.
- **Snowball Strategy Simulation:** Simulate loan payoff with fixed and extra contributions.
- **Excel Export:** Download the simulation result as an Excel spreadsheet.
- **Robust Architecture:** Clean separation of domain, application, infrastructure, and interface layers.
- **Dockerized:** Ready for containerized deployment with Redis support.
- **Production-Ready:** Easily deployable on any server or cloud with Docker.
- **CI/CD Ready:** Designed for integration with GitHub Actions and other CI/CD tools.

---

## 🗂️ Project Structure

```
app/
  domain/         # Domain models and business logic (DDD)
    models.py
    services.py
  application/    # Use cases, DTOs, and exceptions
    use_cases.py
    dto.py
    exceptions.py
  infrastructure/ # (Reserved for DB, external APIs, etc.)
  interface/      # Web layer: Flask routes, app factory, templates
    routes.py
    __init__.py
    templates/
      index.html
  static/
    css/
      style.css
tests/            # Unit and integration tests
Dockerfile
docker-compose.yml
run.py            # App entry point (for local dev)
requirements.txt
```

---

## 🖥️ Local Development

### **Requirements**
- Python 3.11+
- Docker & Docker Compose (recommended for full stack)

### **Quick Start (with Docker Compose)**
```bash
docker-compose up --build
```
- Access the app at [http://localhost:5001](http://localhost:5001)

### **Manual Local Run (without Docker)**
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. (Optional) Start Redis locally if you want session support:
   ```bash
   # Ubuntu/Debian
   sudo apt install redis-server
   sudo systemctl start redis-server
   ```
3. Run the app:
   ```bash
   export REDIS_HOST=localhost
   python run.py
   ```
   - Access at [http://localhost:5001](http://localhost:5001)

---

## 🐳 Production Deployment

### **With Docker Compose (Recommended)**
- On your server:
  ```bash
  docker-compose up -d --build
  ```
- This will start both the web app and Redis.

### **Standalone Container**
- If using an external Redis or local Redis on the server:
  ```bash
  docker run -d \
    -p 5001:5001 \
    -e REDIS_HOST=your-redis-host \
    -e FLASK_ENV=production \
    your-image-name
  ```

---

## ⚙️ Environment Variables

| Variable      | Description                        | Example                |
|---------------|------------------------------------|------------------------|
| REDIS_HOST    | Redis hostname or IP               | redis / localhost      |
| REDIS_PORT    | Redis port                         | 6379                   |
| FLASK_ENV     | Flask environment                  | production / development|
| FLASK_APP     | Flask app factory (if needed)      | app.interface:create_app|

---

## 🧩 Architecture Overview

- **Domain Layer:** Business entities and rules (`app/domain/`)
- **Application Layer:** Use cases, DTOs, orchestration (`app/application/`)
- **Interface Layer:** Flask routes, templates, static files (`app/interface/`)
- **Infrastructure Layer:** (Reserved for DB, APIs, etc.)

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📝 Customization

- **Add new loan types or strategies:** Extend `app/domain/models.py` and `app/domain/services.py`.
- **Add new endpoints:** Create new use cases in `app/application/use_cases.py` and routes in `app/interface/routes.py`.
- **Change UI:** Edit `app/interface/templates/index.html` and `app/static/css/style.css`.

---

## 🛠️ Troubleshooting

- **Redis connection errors:**  
  - Ensure Redis is running and `REDIS_HOST` is set correctly.
  - The app will fall back to filesystem sessions if Redis is unavailable.

- **Port already in use:**  
  - Change the published port in `docker-compose.yml` or `run.py`.

- **Static files or templates not found:**  
  - Ensure your Docker image copies all necessary files and folders.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Contributing

Pull requests and suggestions are welcome!  
Open an issue or submit a PR on GitHub.

---
