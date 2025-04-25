# Multi-Tenant E-commerce API

## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Redis (if not already installed):**

    - **For Linux (Ubuntu/Debian):**
      ```bash
      sudo apt update
      sudo apt install redis-server
      ```

    - **For macOS (using Homebrew):**
      ```bash
      brew install redis
      ```

    - **For Windows:**
      You can use [Redis for Windows](https://github.com/microsoftarchive/redis/releases) or install Redis via Windows Subsystem for Linux (WSL).

    After installing Redis, start the Redis server by running:
    ```bash
    redis-server
    ```

5. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run Celery Worker:**

    Open a terminal window and start the Celery worker with the following command:

    ```bash
    celery -A config.celery worker --loglevel=info
    ```

    Replace `your_project_name` with the name of your Django project.

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application should now be running at `http://127.0.0.1:8000/`.

---
## Swagger UI Documentation

You can access the Swagger documentation for the API at:

```bash
http://localhost:8000/docs/swagger/
```
## Redoc UI Documentation

You can access the Swagger documentation for the API at:

```bash
http://localhost:8000/docs/redoc/
```

## API Endpoints

### Orders

- **GET** `/api/orders/`: List all orders *(only Admin)
- **POST** `/api/orders/`: Create a new order *(Only Customer)
- **GET** `/api/orders/{id}/`: Retrieve an order by ID *(only Admin)
- **PUT** `/api/orders/{id}/`: Update an order by ID *(only Admin)
- **PATCH** `/api/orders/{id}/`: Partially update an order by ID *(only Admin)
- **DELETE** `/api/orders/{id}/`: Delete an order by ID *(Only Admin)
- **POST** `/api/orders/{id}/update_status/`: Update the status of an order *(Only Admin)
- **GET** `/api/orders/my_orders/`: List orders for the current user *(Only Customer)
- **GET** `/api/orders/vendor_orders/`: List orders for the current vendor *(Only Vendor)

### Products

- **GET** `/api/products/`: List all products *(Anyone)
- **POST** `/api/products/`: Add a new product *(Only Vendor)
- **GET** `/api/products/{slug}/`: Retrieve a product by slug *(Anyone)
- **PUT** `/api/products/{slug}/`: Update a product by slug *(Only Vendor)
- **PATCH** `/api/products/{slug}/`: Partially update a product by slug *(Only Vendor)
- **DELETE** `/api/products/{slug}/`: Delete a product by slug *(Only Vendor)
- **GET** `/api/products/my_products/`: List products for the current vendor *(Only Vendor)

### Users

- **GET** `/api/users/`: List all users *(Only Admin)
- **POST** `/api/users/`: Create a new user *(Only Admin)
- **GET** `/api/users/{id}/`: Retrieve a user by ID *(Only Admin)
- **PUT** `/api/users/{id}/`: Update a user by ID *(Only Admin)
- **PATCH** `/api/users/{id}/`: Partially update a user by ID *(Only Admin)
- **DELETE** `/api/users/{id}/`: Delete a user by ID *(Only Admin)
- **POST** `/api/users/auth/login/`: User login *(Anyone)
- **POST** `/api/users/auth/register/admin/`: Register an admin user *(Anyone, Not logged in)
- **POST** `/api/users/auth/register/customer/`: Register a customer user *(Anyone, Not logged in)

### Vendors

- **GET** `/api/vendors/`: List all vendors *(Anyone)
- **POST** `/api/vendors/`: Register a new vendor *(Anyone, Not logged in)
- **GET** `/api/vendors/{slug}/`: Retrieve a vendor by slug *(Anyone)
- **PUT** `/api/vendors/{slug}/`: Update a vendor by slug *(Only vendor)
- **PATCH** `/api/vendors/{slug}/`: Partially update a vendor by slug *(Only vendor)
- **DELETE** `/api/vendors/{slug}/`: Delete a vendor by slug *(Only Admin)

---