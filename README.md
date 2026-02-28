# Fastwork.id Automation & Scraper Package

A standalone Python tool using Playwright to scrape public data and manage a seller account on Fastwork.id. Designed to be easily integrated into Openclaw or other autonomous AI agents.

## Features

- **Authentication Manager**: Logs in via Playwright and saves session cookies so you don't have to authenticate every run.
- **Data Scraper**: Search for services and scrape freelancer profiles.
- **Seller Center Manager**:
  - Read dashboard statistics (active orders, revenue).
  - List all services/products.
  - Edit service prices and titles dynamically.
- **Messaging & Orders Manager**:
  - Fetch active order details.
  - Read unread messages from buyers.
  - Send direct messages.
  - Built-in `auto_reply` method based on keyword mapping.

## Dependencies

- Python 3.8+
- Playwright

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. To see an example run:
   ```bash
   python example.py
   ```

## Usage in Openclaw or AI Tools

You can map functions directly into your AI Agent's toolkit:

```python
from fastwork import FastworkClient

def get_my_fastwork_orders():
    with FastworkClient(headless=True) as fw:
        if not fw.auth.is_logged_in():
            return "Not logged in! Please authenticate first."
        return fw.orders.get_active_orders()
```

## Disclaimer

This project relies on DOM selectors which may change if Fastwork.id updates its interface. Please review the selectors in `scraper.py`, `messaging.py`, and `seller_center.py` if scripts break.
