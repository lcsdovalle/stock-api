
# Stock API

A backend service that lavarages core endpoints for creating, editting, and updating:
- Products
- Customers
- Stock operations

This also sends quotes to customers by email and whatsapp.

![PyPI - Version](https://img.shields.io/pypi/v/django)


## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [License](#license)

## Features
- RESTful API endpoints for CRUD operations
- Secure environment variable handling
- CORS support for multiple origins
- Integration with WhatsApp bot (Venon)
- Comprehensive unit and integration tests
- Docker support for easy deployment


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lcsdovalle/stock-api.git
   cd stock-api/src

2. Install dependencies using poetry:
    `poetry install`

3. Set up environment variables
    ```bash
    cp .env.example .env

4. Run the migrations
    ```bash
    python manage.py migrate
5. Run the server
    ```bash
    python manage.py migrate

---

6. Usage
    Example:
    ```markdown
    ## Usage

    ### API Endpoints
    - `GET /api/v1/order/orders` - List all stocks
    - `POST api/v1/order/create-order` - Create a new stock

    Example request using `curl`:
    ```bash
    curl -X GET http://localhost:8000/api/v1/order/orders -H "Authorization: Bearer <your_token>"
    ```
    ---


7. Configuration
    ```markdown
    ## Configuration

    Update the `.env` file with your environment-specific settings:

    ```plaintext
    SECRET_KEY=your-secret-key
    DB_NAME=your-database-name
    DB_USER=your-database-user
    DB_PASSWORD=your-database-password
    DB_HOST=your-database-host
    DB_PORT=your-database-port
    EMAIL_HOST=your-email-host
    EMAIL_PORT=your-email-port
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email-user
    EMAIL_HOST_PASSWORD=your-email-password
    VENON_BOT_ENDPOINT=your-venon-bot-endpoint
    ALLOWED_HOSTS=your-allowed-hosts (comma-separated)
    CORS_ALLOWED_ORIGINS=your-cors-allowed-origins (comma-separated)
    ```

---

8. Testing

    ```markdown
    ## Testing

    ```bash
    cd src && poetry run python manage.py test
    ```

9. Code sanitizing
    ```bash
    poetry run isort . && poetry run black . && poetry run flake8 .

10. Next
    - Add pre-commit for sanitizing and testing
    - Increase testing cov
    - Add multitenancy
    - Add swagger documentation
    - Add invoice integration

## Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework used
- [Venon Bot](https://github.com/orkestral/venom) - WhatsApp bot library