import os
import json
from playwright.sync_api import sync_playwright
import json

from .auth import AuthManager
from .seller_center import SellerCenterManager
from .messaging import MessagingManager, OrderManager
from .scraper import Scraper

class FastworkClient:
    def __init__(self, headless: bool = False, session_file: str = "fastwork_session.json"):
        self.headless = headless
        self.session_file = session_file
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        # Sub-modules
        self.auth = None
        self.seller = None
        self.messaging = None
        self.orders = None
        self.scraper = None

    def start(self):
        """Starts the browser and loads session if available."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        
        # Load session if exists
        state = None
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    state = json.load(f)
            except Exception as e:
                print(f"Failed to load session file: {e}")

        if state:
             self.context = self.browser.new_context(storage_state=state)
        else:
             self.context = self.browser.new_context()

        self.page = self.context.new_page()
        
        # Initialize modules
        self.auth = AuthManager(self.page)
        self.seller = SellerCenterManager(self.page)
        self.messaging = MessagingManager(self.page)
        self.orders = OrderManager(self.page)
        self.scraper = Scraper(self.page)

    def stop(self):
        """Saves session and closes the browser."""
        if self.context:
            self.context.storage_state(path=self.session_file)
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
