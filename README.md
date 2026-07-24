# E-commerce API

A Django REST Framework backend for a basic e-commerce workflow: user registration and JWT login, product and category management, per-user carts, order placement, order history, and a mock payment flow.

## Features

- Custom user model with address and address type fields.
- User registration and username/password login.
- JWT access and refresh tokens.
- Product and category catalog endpoints.
- Staff-only product and category administration through the API.
- One cart per user with add, update, list, and remove operations.
- Stock validation when adding to a cart and placing an order.
- Order creation from the authenticated user's cart.
- Order history and order detail views for customers.
- Admin order listing, order detail, and order-item status updates.
- Mock payment result handling with `success` and `failure` outcomes.
- Django admin registrations for users, catalog, carts, and orders.

## Tech Stack

- Python
- Django
- Django REST Framework
- `djangorestframework-simplejwt`
- SQLite

The repository does not currently include a `requirements.txt` or other dependency lockfile. Install the dependencies required by the imports above in your environment before running the project.

## Project Structure

```text
.
├── cart/            # Per-user carts and cart items
├── e_commerce/      # Django project configuration
├── orders/          # Orders, order items, and order services
├── products/        # Categories and products
├── users/           # Custom user, registration, and login
├── db.sqlite3       # SQLite database included in the repository
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3 and a compatible Django environment. The repository does not pin a Python or package version.
- A virtual environment.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install Django djangorestframework djangorestframework-simplejwt
```

Run the migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/`.

### Create an admin user

Create a Django superuser to access `/admin/` and the staff-only API operations:

```bash
python manage.py createsuperuser
```

## Authentication

The API uses JWT authentication for protected DRF endpoints. Obtain tokens with either the custom login endpoint or Simple JWT's token endpoint:

```http
POST /login/
Content-Type: application/json

{
  "username": "alice",
  "password": "your-password"
}
```

The custom login response includes `access_token`, `refresh_token`, and basic user information. The standard token endpoints are also available:

- `POST /api/token/` obtains an access and refresh token pair.
- `POST /api/token/refresh/` obtains a new access token from a refresh token.

Send the access token on protected requests:

```http
Authorization: Bearer <access_token>
```

Access tokens are configured to expire after one day. Registration is public; catalog, cart, and order operations require authentication unless noted otherwise.

## API Reference

All endpoints return JSON. Successful responses generally wrap serialized data in a `data` field and may include a `message` field. Validation errors are returned by Django REST Framework.

### Users

#### Register

```http
POST /register/
```

Request fields:

```json
{
  "username": "alice",
  "password": "your-password",
  "first_name": "Alice",
  "last_name": "Example",
  "email": "alice@example.com",
  "address": "1 Example Street",
  "address_type": "home"
}
```

`address_type` accepts `home`, `work`, or `other`. The response includes the generated user ID and the read-only `fullname` value.

#### Login

```http
POST /login/
```

Request fields are `username` and `password`.

### Products and Categories

All catalog endpoints require an authenticated user. Product creation, editing, and deletion require a staff user. Category creation requires a staff user, and category replacement or deletion require a user with `is_staff=True`.

| Method   | Endpoint                     | Access        | Description                 |
| -------- | ---------------------------- | ------------- | --------------------------- |
| `GET`    | `/products/`                 | Authenticated | List all products.          |
| `POST`   | `/products/`                 | Staff         | Create a product.           |
| `GET`    | `/products/<product_id>/`    | Authenticated | Retrieve one product.       |
| `PATCH`  | `/products/<product_id>/`    | Staff         | Partially update a product. |
| `DELETE` | `/products/<product_id>/`    | Staff         | Delete a product.           |
| `GET`    | `/categories/`               | Authenticated | List all categories.        |
| `POST`   | `/categories/`               | Staff         | Create a category.          |
| `PUT`    | `/categories/<category_id>/` | Staff         | Replace a category.         |
| `DELETE` | `/categories/<category_id>/` | Staff         | Delete a category.          |

`GET /products/` accepts the optional `category` query parameter, which filters by category ID, for example `/products/?category=2`.

Product fields are `name`, `description`, `price`, `stock_quantity`, and `category`. Category fields are `name` and the generated `id`. Product prices must be at least `0.01`; stock is a non-negative integer. Category names are unique, and a category cannot be deleted while products still reference it.

### Cart

Cart endpoints require authentication and operate only on the requesting user's cart.

| Method   | Endpoint                      | Description                         |
| -------- | ----------------------------- | ----------------------------------- |
| `GET`    | `/cart-items/`                | List the current user's cart items. |
| `POST`   | `/cart-items/`                | Add a product to the cart.          |
| `PATCH`  | `/cart-items/<cart_item_id>/` | Set a cart item's quantity.         |
| `DELETE` | `/cart-items/<cart_item_id>/` | Remove a cart item.                 |

Add an item with:

```json
{
  "product": 1,
  "quantity": 2
}
```

Adding the same product again increases its existing quantity. Quantities must be greater than zero and cannot exceed available stock. Cart item responses include product summary information (`id`, `name`, and `price`), `quantity`, and calculated `sub_total`.

### Orders

Customer order endpoints require authentication and are scoped to the requesting user. Administrative order endpoints require a user with `is_staff=True`.

| Method  | Endpoint                              | Access        | Description                                |
| ------- | ------------------------------------- | ------------- | ------------------------------------------ |
| `POST`  | `/orders/place/`                      | Authenticated | Create an order from the current cart.     |
| `GET`   | `/orders/`                            | Authenticated | List the current user's order history.     |
| `GET`   | `/orders/<order_id>/`                 | Authenticated | Retrieve one of the current user's orders. |
| `POST`  | `/orders/<order_id>/pay/`             | Authenticated | Submit a mock payment result.              |
| `GET`   | `/orders/admin/`                      | Staff         | List all orders.                           |
| `GET`   | `/orders/<order_id>/admin/`           | Staff         | Retrieve any order and its items.          |
| `PATCH` | `/order-items/<order_item_id>/admin/` | Staff         | Update an order item's status.             |

Place an order with:

```json
{
  "shipping_address": "1 Example Street"
}
```

Placing an order requires a non-empty cart and sufficient stock for every item. The operation creates the order and its items, records each product's current price as `bought_price`, decreases product stock, and clears the cart in one database transaction. New orders and order items start with `pending` status.

Supported order payment statuses are `pending`, `paid`, `cancelled`, and `partially_cancelled`. Supported order-item statuses are `pending`, `shipped`, `delivered`, `returned`, and `cancelled`.

The payment endpoint accepts only:

```json
{
  "result": "success"
}
```

or:

```json
{
  "result": "failure"
}
```

A `success` result changes a pending order to `paid`. A `failure` result returns a payment error, and attempting to pay an order whose payment status is no longer pending returns an error. This is a mock payment flow; no external payment provider is configured.

## Django Admin

The Django admin is available at:

```text
http://127.0.0.1:8000/admin/
```

The admin site registers the custom users, categories, products, carts, cart items, orders, and order items.

## Configuration

The current development configuration:

- Uses SQLite at `db.sqlite3`.
- Uses `users.CustomUser` as `AUTH_USER_MODEL`.
- Enables JWT authentication as the default DRF authentication class.
- Sets `DEBUG = True` and leaves `ALLOWED_HOSTS` empty.
- Uses UTC and Django timezone support.

Before deploying beyond local development, configure a production secret key, disable debug mode, set allowed hosts, and review the database and other Django deployment settings.

## Testing

Run the Django test suite with:

```bash
python manage.py test
```

The app test modules currently contain only empty `TestCase` scaffolds, so automated behavior coverage is not yet implemented in the repository.

## License

No license file is currently included in the repository.
