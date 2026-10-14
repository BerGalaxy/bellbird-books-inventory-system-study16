# Bellbird Books Inventory and Customer Order System

## Project Overview
A web-based inventory and customer order system for Bellbird Books, an independent bookstore. It distinguishes new books (quantity-based) from second-hand books (unique items).

## Features
- New books managed by quantity (selling reduces count)
- Second-hand books recorded as individual copies with unique condition and price
- Customer order management with status transitions: Ordered → Arrived → Picked up
- Partial title/author search across both new and second-hand stock
- Order edit and cancel
- Shop area filtering

## Prerequisites
- Python 3.x
- Git

## Tech Stack
- Python (Flask)
- SQLite
- Pytest

## Project Structure
- `app/` — Flask application (models, routes, templates)
- `tests/` — Automated tests
- `seed_data.py` — Database initialisation with sample data
- `config.py` — Configuration settings
- `deploy.sh` — Deployment script
- `CHANGELOG.md` — Version history

## How to Run
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize the database with sample data: `python seed_data.py`
6. Run the app: `python run.py`
7. Open `http://127.0.0.1:5000`

## How to Test
Run `pytest tests/test_inventory.py -v` in the terminal.

## Deployment
See `deploy.sh` for deployment steps.

## Team
- Tongqi Zhang — Product Owner, Architecture, Configuration Management
- Minghang Li — CRUD, Order Management
- Yuxuan Feng — Testing, Search & Filtering

## Project
ISYS3001 Study 16 — Bellbird Books Inventory and Customer Order System