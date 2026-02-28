from playwright.sync_api import Page
from typing import List, Dict, Any
import time

class SellerCenterManager:
    def __init__(self, page: Page):
        self.page = page

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Navigates to the seller dashboard and extracts key metrics.
        Returns a dictionary with status pekerjaan, metrics, and useful links.
        """
        self.page.goto("https://seller.fastwork.id/dashboard")
        self.page.wait_for_load_state("domcontentloaded")
        
        # NOTE: Selectors must be updated based on real page structure
        # These are illustrative selectors for a generic dashboard
        stats = {}
        try:
            # Using specific text locators confirmed by visual inspection
            # "Order yang sedang berjalan" -> Next sibling div contains the count
            active = self.page.locator('div:has-text("Order yang sedang berjalan") + div').first.inner_text()
            stats["active_orders"] = active

            # "akumulasi pendapatan" -> Next sibling div contains the money
            revenue = self.page.locator('div:has-text("akumulasi pendapatan") + div').first.inner_text()
            stats["total_earned"] = revenue
        except:
             print("Could not parse dashboard stats. Selectors may need updating.")
        
        return stats

    def get_products(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of products (jasa) offered by the seller.
        """
        self.page.goto("https://seller.fastwork.id/my-services")
        self.page.wait_for_load_state("domcontentloaded")
        
        products = []
        try:
            # Look for rows in the trb-table
            product_rows = self.page.locator("table.trb-table tbody tr")
            self.page.wait_for_timeout(2000) # Give table time to render data
            count = product_rows.count()
            
            for i in range(count):
                row = product_rows.nth(i)
                # Column 1 contains the title and link
                col1 = row.locator("td").nth(0)
                link_elem = col1.locator("a").first
                
                # Take inner_text of the entire column in case the link only wraps an image
                title_raw = col1.inner_text().strip()
                title = title_raw.split('\n')[0] if title_raw else "Unknown Title"
                
                url_path = link_elem.get_attribute("href") if link_elem.count() > 0 else ""
                full_url = f"https://fastwork.id{url_path}" if url_path.startswith("/") else url_path
                
                # Column 3 contains the status
                col3 = row.locator("td").nth(2)
                status = col3.inner_text().strip()
                
                products.append({
                    "title": title,
                    "status": status,
                    "url": full_url
                })
        except Exception as e:
            print(f"Could not parse products: {e}")
            
        return products

    def edit_product(self, product_url: str, new_title: str = None, new_price: str = None):
        """
        Navigates to a specific product edit page and updates it.
        """
        self.page.goto(product_url)
        self.page.click("text='Edit Jasa'")
        self.page.wait_for_load_state("domcontentloaded")
        
        try:
            if new_title:
                title_input = self.page.locator("input[name='title']")
                title_input.fill(new_title)
                
            if new_price:
                price_input = self.page.locator("input[name='price']")
                price_input.fill(new_price)
                
            # Save changes
            self.page.click("button:has-text('Simpan')")
            print(f"Product {product_url} successfully updated.")
            time.sleep(2) # Give it time to save to DB
        except Exception as e:
            print(f"Failed to edit product: {e}")
