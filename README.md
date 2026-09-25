# Bellbird Books Inventory and Customer Order System

## Project Overview
A web-based inventory and customer order system for Bellbird Books, an independent bookstore. It distinguishes new books (quantity-based) from second-hand books (unique items).

## Tech Stack
- Python (Flask)
- SQLite
- Pytest

## Project Structure
- `app/` — Flask application (models, routes)
- `tests/` — Automated tests
- `config.py` — Configuration settings
- `deploy.sh` — Deployment script
- `CHANGELOG.md` — Version history

## How to Run
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python run.py`
6. Open `http://127.0.0.1:5000`

## How to Test
Run `pytest tests/test_inventory.py -v` in the terminal.

## Deployment
See `deploy.sh` for deployment steps.