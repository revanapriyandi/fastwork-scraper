from playwright.sync_api import Page, expect
import time

class AuthManager:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username, password):
        """
        Navigates to the login page and performs login.
        Waits for successful login indicators (like navigation to dashboard).
        """
        print(f"Logging in as {username}...")
        self.page.goto("https://fastwork.id/")
        
        try:
            # Click the login link on the homepage
            self.page.click("#login-link, a[href*='/login']")
            
            # Step 1: Email
            self.page.fill("input[placeholder='Masukkan email atau nomor telepon']", username)
            self.page.click("button:has-text('Lanjutkan')")
            
            # Step 2: Password
            self.page.fill("input[placeholder='Kata Sandi']", password)
            self.page.click("button:has-text('Lanjutkan')")
            
            # Wait for login link to disappear (indicates successful login)
            print("Password submitted, waiting for authentication callback...")
            login_link = self.page.locator("#login-link, a[href*='/login']")
            login_link.first.wait_for(state="hidden", timeout=15000)
            
            # Verify login success by checking for some profile element
            # Example: wait for a generic user avatar or dropdown to prove login
            print("Login flow completed. Checking session...")
            
            # Small delay to ensure cookies are set
            time.sleep(2)
            
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            # If Fastwork has captchas or OTPs, they should be handled here manually 
            # or by pausing and asking the user to solve them on the first run.
            return False

    def is_logged_in(self) -> bool:
        """
        Checks if the current session is authenticated by verifying the presence of 
        user-specific elements on the homepage.
        """
        self.page.goto("https://fastwork.id/")
        self.page.wait_for_load_state("domcontentloaded")
        
        # Since Fastwork auto-redirects to /seller/dashboard when logged in
        # or stays on / if home. Let's check for 'login-link'
        try:
            # Use a short timeout
            login_link = self.page.locator("#login-link")
            if login_link.count() > 0 and login_link.first.is_visible(timeout=3000):
                return False
            return True
        except Exception:
             # Fast fail, likely logged in if no explicit login elements found
             return True
