# spareParts_final

A Django‑based web application for managing spare‑part inventory, sales, and purchase transactions. The project demonstrates a full CRUD workflow, custom forms, and profit calculations for a small workshop or parts retailer.

---

## Overview

`spareParts_final` is a Python/Django project that allows users to:

- Register and maintain a catalog of spare parts.
- Record purchases and sales with automatic profit calculations.
- Generate simple reports on inventory status and financial performance.

The repository contains the complete source code, migration history, and a brief project description (`Project File.docx`). A compressed archive (`Spareparts_final.rar`) is also provided for quick extraction.

---

## Features

| Feature | Description |
|---------|-------------|
| **Inventory Management** | Add, edit, delete spare‑part records (name, description, price, stock). |
| **Purchase & Sale Tracking** | Record purchase orders and sales invoices; the system updates stock levels automatically. |
| **Profit Calculation** | Automatic computation of purchase profit and sale profit per item. |
| **Custom Forms** | Django forms with validation for purchase, sale, and spare‑part data. |
| **Admin Interface** | Full CRUD access via Django admin for rapid data entry. |
| **Database Migrations** | Seven migration files handling schema evolution and data cleanup. |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9 |
| **Framework** | Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Front‑end** | Django templates (HTML/CSS) |
| **Version Control** | Git |
| **Packaging** | `requirements.txt` (generated from the environment) |

---

## Installation

> **Note:** The steps assume you have Python 3.9+ and Git installed on your machine.

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/spareParts_final.git
   cd spareParts_final
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is missing, you can install Django directly:*

   ```bash
   pip install Django
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files (optional for production)**

   ```bash
   python manage.py collectstatic
   ```

---

## Usage

### Run the development server

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/` to explore the application.

### Admin interface

If you created a superuser, access the admin panel at `http://127.0.0.1:8000/admin/` to manage spare parts, purchases, and sales directly.

### Core URLs (default)

| URL | Purpose |
|-----|---------|
| `/` | Home page – overview of inventory status |
| `/spareparts/` | List, add, edit, delete spare parts |
| `/purchases/` | Record new purchase orders |
| `/sales/` | Record new sales invoices |
| `/reports/` | Simple profit and stock reports (if implemented) |

*All URLs are defined in `myapp/urls.py`.*

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details